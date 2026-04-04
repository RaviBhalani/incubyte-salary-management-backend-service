# Serializer Conventions

## Field Exposure

Default to `fields = "__all__"` for simple resources. Use an explicit list when:
- Some fields must be write-only (e.g., passwords)
- Some fields must never be exposed (internal flags)
- The response shape differs meaningfully from the model

```python
class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
```

## Read vs Write Serializers

When create/update input shape differs from read output, define two serializers and switch in the viewset via `get_serializer_class`:

```python
class ProductWriteSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "price", "category"]

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
```

In the viewset:
```python
def get_serializer_class(self):
    if self.action in ("create", "update", "partial_update"):
        return ProductWriteSerializer
    return ProductSerializer
```

## Related Field Serialization (FK, O2O, M2M)

Related field serialization applies **only to read serializers**. Write serializers accept raw PKs with no modifications — never declare nested serializers or `read_only` fields on a write serializer.

**Read serializer** — import and use the serializer from the related object's own app. Every FK, O2O, and M2M field must be explicitly declared — do not leave any related field to DRF's default PK representation in the read serializer:

```python
from apps.catalog.serializers import CategorySerializer, TagSerializer
from apps.user.serializers import UserSerializer

class ProductSerializer(ModelSerializer):       # read serializer
    category = CategorySerializer(read_only=True)        # FK / O2O
    owner = UserSerializer(read_only=True)               # FK / O2O
    tags = TagSerializer(many=True, read_only=True)      # M2M — many=True required

    class Meta:
        model = Product
        fields = "__all__"
```

**Write serializer** — plain fields only, no nested serializers:

```python
class ProductWriteSerializer(ModelSerializer):  # write serializer
    class Meta:
        model = Product
        fields = ["name", "price", "category", "owner", "tags"]
```

## M2M Write Pattern

Pop M2M data before creating, then set after:

```python
def create(self, validated_data):
    tag_ids = validated_data.pop("tags", [])
    instance = Product.objects.create(**validated_data)
    instance.tags.set(tag_ids)
    return instance

def update(self, instance, validated_data):
    tag_ids = validated_data.pop("tags", None)
    instance = super().update(instance, validated_data)
    if tag_ids is not None:
        instance.tags.set(tag_ids)
    return instance
```

## Validation

Use `validate_<field>` for single-field validation and `validate` for cross-field:

```python
def validate_price(self, value):
    if value < 0:
        raise serializers.ValidationError("Price must be non-negative.")
    return value

def validate(self, attrs):
    if attrs["end_date"] < attrs["start_date"]:
        raise serializers.ValidationError("end_date must be after start_date.")
    return attrs
```
