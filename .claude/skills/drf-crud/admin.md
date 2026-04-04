# Admin Conventions

Admin classes are extensive by design — they serve as the primary development and debugging interface. Err on the side of more fields, more filters, more search.

## Registration

Always use the `@admin.register` decorator — never `admin.site.register`:

```python
from django.contrib import admin
from apps.product.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ...
```

## Standard Admin Class

Every admin class must include all of the following attributes:

```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # --- List view ---
    list_display = ("id", "name", "category", "price", "is_active", "created_by", "created_ts", "modified_ts")
    list_filter = ("is_active", "category", "created_ts")
    search_fields = ("id", "name", "category__name", "created_by__email")
    ordering = ("-created_ts",)
    date_hierarchy = "created_ts"
    list_per_page = 50
    list_select_related = ("category", "created_by")
    show_full_result_count = True
    save_on_top = True

    # --- Detail view ---
    readonly_fields = ("id", "created_ts", "modified_ts", "created_by", "modified_by")
    autocomplete_fields = ("category",)
    fieldsets = (
        ("Core", {"fields": ("id", "name", "price", "description")}),
        ("Relations", {"fields": ("category", "tags")}),
        ("Status", {"fields": ("is_active",)}),
        ("Audit", {"fields": ("created_by", "modified_by", "created_ts", "modified_ts")}),
    )
```

## Attribute Rules

**`list_display`** — always start with `id`, include all meaningful fields, always end with `created_ts` and `modified_ts`. Include FK fields directly (Django renders them via `__str__`).

**`list_filter`** — include all boolean fields, all FK fields, and `created_ts`. Use `list_filter` generously — it costs nothing and saves debug time.

**`search_fields`** — include `id` (as `"id"` not `"=id"`), all `CharField`/`TextField` fields, and FK traversals for the most commonly searched related fields (e.g. `"category__name"`, `"created_by__email"`).

**`readonly_fields`** — always include `id`, all `Timestamps` fields (`created_ts`, `modified_ts`), and all `CreatedBy`/`ModifiedBy` fields. These must never be editable in the admin.

**`autocomplete_fields`** — use for all FK and O2O fields in the form. Requires the related model's admin to define `search_fields`.

**`list_select_related`** — list every FK that appears in `list_display` to avoid N+1 queries.

**`date_hierarchy`** — set to `"created_ts"` when the model inherits `Timestamps`.

**`autocomplete_fields`** — use for FK and O2O fields in the form (requires the related admin to have `search_fields` defined).

**`filter_horizontal`** — use for M2M fields in the form. Renders a dual-list widget that is far easier to use than the default multi-select:

```python
filter_horizontal = ("tags", "items")
```

**`fieldsets`** — always group fields into logical sections. Suggested sections:
- `Core` — the model's primary data fields
- `Relations` — FK, O2O, M2M fields
- `Status` — boolean flags
- `Audit` — readonly timestamp and user-tracking fields

## Inlines

Use `TabularInline` for compact related records (many rows expected), `StackedInline` for complex related records (few rows, many fields each):

```python
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = True
    readonly_fields = ("created_ts",)
    fields = ("product", "quantity", "unit_price", "created_ts")
```

Always set `extra = 0` — adding blank rows by default clutters the debug view.

Add inlines to the parent admin via `inlines`:

```python
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    ...
```

## Custom Display Methods

Use `@admin.display` to compute or format values for `list_display`:

```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "tag_count", ...)

    @admin.display(description="Tags")
    def tag_count(self, obj):
        return obj.tags.count()
```

For boolean fields, add `boolean=True` to get a tick/cross icon:

```python
@admin.display(description="Published", boolean=True)
def is_published(self, obj):
    return obj.status == "published"
```
