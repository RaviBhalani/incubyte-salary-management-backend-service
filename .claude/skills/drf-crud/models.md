# Model Conventions

## Mixin Selection

Import: `from apps.core.models import Timestamps, CreatedBy, ModifiedBy, IsActive`

| Mixin | Fields added | Use when |
|-------|-------------|----------|
| `Timestamps` | `created_ts` (auto), `modified_ts` (auto) | Almost always — provides audit trail |
| `CreatedBy` | `created_by` FK → User (nullable) | Need to track who created the record |
| `ModifiedBy` | `modified_by` FK → User (nullable) | Need to track who last edited |
| `IsActive` | `is_active` bool (default `True`) | Soft-delete pattern instead of hard deletes |

**Selection guide:**
- Default new resource: `Timestamps` only
- User-owned resource: add `CreatedBy`
- Editable by multiple users: add `ModifiedBy`
- Soft-deletable: add `IsActive`
- Combine freely — no mandatory set

```python
class Product(Timestamps, CreatedBy, IsActive):
    ...
```

## Meta Class

Always set `db_table` to the snake_case singular model name:

```python
class Meta:
    db_table = "product"
```

Add `ordering` when a default sort order makes sense for the resource:

```python
class Meta:
    db_table = "product"
    ordering = ["-created_ts"]
```

Add `indexes` for fields used in frequent filter/lookup queries:

```python
class Meta:
    db_table = "product"
    indexes = [
        models.Index(fields=["category_id", "is_active"]),
    ]
```

## Field Conventions

**General rule — no redundant defaults:** Only write a kwarg when its value differs from Django's default. Never write `null=False`, `blank=False`, `editable=True`, etc. explicitly.

```python
# bad
name = models.CharField(max_length=255, null=False, blank=False)
# good
name = models.CharField(max_length=255)
```

---

**CharField / TextField** — `max_length` is mandatory on both:

```python
name = models.CharField(max_length=255)
notes = models.TextField(max_length=2000, blank=True)
```

---

**ForeignKey** — singular name (no `_id` suffix), `related_name` and `on_delete` are mandatory:

```python
category = models.ForeignKey(
    "catalog.Category",
    on_delete=models.CASCADE,
    related_name="products",
)
# optional FK
owner = models.ForeignKey(
    "user.User",
    on_delete=models.SET_NULL,
    related_name="owned_products",
    null=True,
)
```

---

**OneToOneField** — same rules as FK: singular name, no `_id`, `related_name` and `on_delete` mandatory:

```python
profile = models.OneToOneField(
    "user.User",
    on_delete=models.CASCADE,
    related_name="product_profile",
)
```

---

**ManyToManyField** — plural name, no `_id` or other suffix, `related_name` mandatory:

```python
tags = models.ManyToManyField("catalog.Tag", related_name="products")
```

---

**BooleanField** — name must start with `is_`, `has_`, `can_`, `should_`, or another intent-clear prefix:

```python
is_active = models.BooleanField(default=True)
has_discount = models.BooleanField(default=False)
can_be_returned = models.BooleanField(default=True)
```

---

## __str__ Method

Every model must define `__str__`. Return the most human-identifiable field — typically `name`, `title`, or a short composite:

```python
def __str__(self):
    return self.name                        # single identifying field

def __str__(self):
    return f"{self.first_name} {self.last_name}"   # composite

def __str__(self):
    return f"Order #{self.id} — {self.status}"     # when no name field exists
```
