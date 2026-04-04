# Viewset Conventions

## BaseViewset vs Partial Mixins

Use `BaseViewset` when all 5 CRUD operations are needed — it includes JWT auth, pagination, and ordering by default:

```python
from apps.core.views import BaseViewset

class ProductViewset(BaseViewset):
    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    ordering = ["-modified_ts"]
```

Use individual mixins with `GenericViewSet` when only a subset of operations is needed. Always include `BaseOrderingFilterMixin` first to preserve ordering and filter behaviour:

```python
from rest_framework.viewsets import GenericViewSet
from apps.core.views import BaseListModelMixin, BaseCreateModelMixin, BaseOrderingFilterMixin

class ProductReadCreateViewset(BaseOrderingFilterMixin, BaseListModelMixin, BaseCreateModelMixin, GenericViewSet):
    http_method_names = ["get", "post"]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
```

Available action mixins: `BaseListModelMixin`, `BaseRetrieveModelMixin`, `BaseCreateModelMixin`, `BaseUpdateModelMixin`, `BaseDestroyModelMixin`

**`http_method_names` is mandatory on every viewset.** List only the HTTP methods the viewset actually handles. Common values:

| Operations present | http_method_names |
|--------------------|-------------------|
| Full CRUD | `["get", "post", "patch", "delete"]` |
| Read-only | `["get"]` |
| Read + Create | `["get", "post"]` |
| Read + Update | `["get", "patch"]` |

Use `patch` (not `put`) — partial update is the standard in this project.

## get_serializer_class

Always use `get_serializer_class` to select between read and write serializers — never set `serializer_class` alone when a read/write split exists:

```python
from apps.product.serializers import ProductSerializer, ProductWriteSerializer

class ProductViewset(BaseViewset):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Product.objects.all()
    ordering = ["-modified_ts"]

    def get_serializer_class(self):
        if self.action in (CREATE, UPDATE, PARTIAL_UPDATE):
            return ProductWriteSerializer
        return ProductSerializer
```

Import the action name constants from `apps.core.constants` — never use raw strings in `get_serializer_class`:

```python
from apps.core.constants import CREATE, PARTIAL_UPDATE, UPDATE
```

`apps/core/constants.py` defines: `CREATE = 'create'`, `UPDATE = 'update'`, `PARTIAL_UPDATE = 'partial_update'`, `LIST = 'list'`, `RETRIEVE = 'retrieve'`, `DESTROY = 'destroy'`.

When only one serializer is needed (read-only viewset or no input/output shape difference), `serializer_class` is sufficient.

## Ordering

`BaseViewset` inherits `BaseOrderingFilterMixin` which sets:
- `filter_backends = (OrderingFilter,)`
- `ordering_fields = ["id"]`
- `ordering = ["-id"]`

Override `ordering` on the viewset to set a resource-appropriate default. Prefer timestamp fields:

```python
ordering = ["-modified_ts"]   # most recently updated first
ordering = ["-created_ts"]    # most recently created first
```

Extend `ordering_fields` to allow clients to sort by additional columns:

```python
ordering_fields = ["id", "name", "created_ts"]
```

## get_queryset Override

Override `get_queryset` to filter by the authenticated user, apply `select_related`/`prefetch_related`, or scope by URL kwargs:

```python
def get_queryset(self):
    return Product.objects.filter(
        created_by=self.request.user,
        is_active=True,
    ).select_related("category")
```

Always call `super().get_queryset()` when you need to preserve base ordering or annotations defined elsewhere.

## Custom Actions

Use `@action` for non-CRUD endpoints on a resource:

```python
from rest_framework.decorators import action
from rest_framework.response import Response

class ProductViewset(BaseViewset):
    ...

    @action(detail=True, methods=["post"], url_path="activate")
    def activate(self, request, pk=None):
        product = self.get_object()
        product.is_active = True
        product.save(update_fields=["is_active"])
        return get_response(data=ProductSerializer(product).data, success=True)
```

- `detail=True` — URL includes `<pk>`, e.g. `/product/5/activate/`
- `detail=False` — URL is collection-level, e.g. `/product/bulk-import/`
- Import `get_response` from `apps.core.custom_exception_handlers` to keep response envelope consistent
