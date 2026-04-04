# Constants Conventions

Every app has a `constants.py`. Any raw value used anywhere in the app is defined there first.

**Rule:** If you are typing a string literal, integer literal, or list literal directly into a non-constants file — stop and define it in `constants.py` first.

---

## models.py

`max_length`, `default`, `help_text`, and `choices` values all come from constants:

```python
# constants.py
PRODUCT_NAME_MAX_LENGTH = 255
PRODUCT_DESCRIPTION_MAX_LENGTH = 2000
PRODUCT_STATUS_MAX_LENGTH = 20

PRODUCT_STATUS_DRAFT = "draft"
PRODUCT_STATUS_PUBLISHED = "published"
PRODUCT_STATUS_CHOICES = [
    (PRODUCT_STATUS_DRAFT, "Draft"),
    (PRODUCT_STATUS_PUBLISHED, "Published"),
]

PRODUCT_PRICE_MAX_DIGITS = 10
PRODUCT_PRICE_DECIMAL_PLACES = 2

PRODUCT_NAME_HELP_TEXT = "Display name of the product"
PRODUCT_STATUS_HELP_TEXT = "Publication status"

# models.py
from apps.product.constants import (
    PRODUCT_DESCRIPTION_MAX_LENGTH,
    PRODUCT_NAME_HELP_TEXT,
    PRODUCT_NAME_MAX_LENGTH,
    PRODUCT_PRICE_DECIMAL_PLACES,
    PRODUCT_PRICE_MAX_DIGITS,
    PRODUCT_STATUS_CHOICES,
    PRODUCT_STATUS_DRAFT,
    PRODUCT_STATUS_HELP_TEXT,
    PRODUCT_STATUS_MAX_LENGTH,
)

class Product(Timestamps):
    name = models.CharField(max_length=PRODUCT_NAME_MAX_LENGTH, help_text=PRODUCT_NAME_HELP_TEXT)
    description = models.TextField(max_length=PRODUCT_DESCRIPTION_MAX_LENGTH, blank=True)
    price = models.DecimalField(
        max_digits=PRODUCT_PRICE_MAX_DIGITS,
        decimal_places=PRODUCT_PRICE_DECIMAL_PLACES,
    )
    status = models.CharField(
        max_length=PRODUCT_STATUS_MAX_LENGTH,
        choices=PRODUCT_STATUS_CHOICES,
        default=PRODUCT_STATUS_DRAFT,
        help_text=PRODUCT_STATUS_HELP_TEXT,
    )
```

`DecimalField` `max_digits` and `decimal_places` are also constants — never hardcode them inline.

---

## apps.py

The app name constant lives in the **app's own `constants.py`** — not in `apps/core/constants.py`. `apps/core/constants.py` only pre-defines `CORE_APP` and `USER_APP`. New apps define their own constant locally and import it in `apps.py`:

```python
# apps/product/constants.py
PRODUCT_APP = "apps.product"

# apps/product/apps.py
from django.apps import AppConfig
from apps.product.constants import PRODUCT_APP

class ProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = PRODUCT_APP
```

For `INSTALLED_APPS` / `PROJECT_APPS` in `settings.py`, import each app's constant from its own constants module:

```python
from apps.core.constants import USER_APP
from apps.product.constants import PRODUCT_APP

PROJECT_APPS = [
    USER_APP,
    PRODUCT_APP,
]
```

---

## serializers.py

All validation error messages are constants — never inline string literals:

```python
# constants.py
PRICE_NEGATIVE_ERROR = "Price must be non-negative."
DATE_RANGE_ERROR = "end_date must be after start_date."

# serializers.py
from apps.product.constants import DATE_RANGE_ERROR, PRICE_NEGATIVE_ERROR

def validate_price(self, value):
    if value < 0:
        raise serializers.ValidationError(PRICE_NEGATIVE_ERROR)
    return value

def validate(self, attrs):
    if attrs["end_date"] < attrs["start_date"]:
        raise serializers.ValidationError(DATE_RANGE_ERROR)
    return attrs
```

---

## urls.py

URL path strings and router basenames are constants:

```python
# constants.py
PRODUCT_URL = "product"
PRODUCT_BASENAME = "product"

# urls.py
from apps.product.constants import PRODUCT_BASENAME, PRODUCT_URL

router = DefaultRouter()
router.register(PRODUCT_URL, ProductViewset, basename=PRODUCT_BASENAME)
```

---

## views.py

`http_method_names` uses the HTTP method constants from `apps/core/constants.py` — never raw strings:

```python
# apps/core/constants.py  (already defined)
GET = "get"
POST = "post"
PATCH = "patch"
DELETE = "delete"

# views.py
from apps.core.constants import DELETE, GET, PATCH, POST

class ProductViewset(BaseViewset):
    http_method_names = [GET, POST, PATCH, DELETE]
    ...
```

---

## Naming Conventions

- ALL_CAPS_SNAKE_CASE for all constants
- Prefix constants with the model or context name to avoid collisions (e.g. `PRODUCT_NAME_MAX_LENGTH` not `NAME_MAX_LENGTH`)

---

## File Structure & Grouping

Constants are grouped by concern in a fixed order. Each group is wrapped in a comment block:

```python
"""
App name
"""
PRODUCT_APP = "apps.product"
"""
App name end
"""

"""
URL constants
"""
PRODUCT_URL = "product"
PRODUCT_BASENAME = "product"
"""
URL constants end
"""

"""
Model constants
"""
PRODUCT_NAME_MAX_LENGTH = 255
PRODUCT_DESCRIPTION_MAX_LENGTH = 2000
PRODUCT_SKU_MAX_LENGTH = 100

PRODUCT_STATUS_DEFAULT = "draft"

STATUS_DRAFT = "draft"
STATUS_PUBLISHED = "published"
STATUS_ARCHIVED = "archived"
PRODUCT_STATUS_CHOICES = [
    (STATUS_DRAFT, "Draft"),
    (STATUS_PUBLISHED, "Published"),
    (STATUS_ARCHIVED, "Archived"),
]

PRODUCT_NAME_HELP_TEXT = "Display name of the product"
PRODUCT_STATUS_HELP_TEXT = "Publication status of the product"
"""
Model constants end
"""

"""
Messages
"""
PRICE_NEGATIVE_ERROR = "Price must be non-negative."
DATE_RANGE_ERROR = "end_date must be after start_date."
"""
Messages end
"""
```

**Standard group order** for an app's `constants.py`:

| Order | Group | Contains |
|-------|-------|----------|
| 1 | App name | The `"apps.<name>"` string |
| 2 | URL constants | Router paths and basenames |
| 3 | Model constants | Field lengths, defaults, choices, help text |
| 4 | Messages | Validation errors and any other user-facing strings |
| 5 | Any other app-specific constants | Grouped by concern with a descriptive header |

Omit a group entirely if the app has no constants of that type — don't add empty blocks.
