---
name: drf-crud
description: Use when creating new CRUD API endpoints in a project generated from the drf-template cookiecutter — given a model name, ER table, or list of fields to expose
---

# DRF CRUD

## Layer Rules

See [models.md](models.md), [serializers.md](serializers.md), [views.md](views.md), [admin.md](admin.md), [constants.md](constants.md) for conventions.

## Overview

`BaseViewset` provides all 5 CRUD operations (list, retrieve, create, update, destroy) with JWT auth and pagination wired in by default. Every new resource needs 4 files: model, serializer, viewset, urls.

## Quick Reference

| File | Path |
|------|------|
| Model | `apps/<app>/models.py` |
| Serializer | `apps/<app>/serializers.py` |
| Viewset | `apps/<app>/views.py` |
| URLs | `apps/<app>/urls.py` |

## App Setup

If the app directory does not yet exist, create it with:
```bash
python manage.py startapp <appname> apps/<appname>
```
This creates `migrations/` and `__init__.py` files. Then overwrite the scaffolded files with the content below.

## Core Pattern — `Tag` Example

A minimal app (no FK/M2M, full CRUD) illustrating all mandatory conventions.

### `apps/tag/constants.py`
```python
"""
App name
"""
TAG_APP = "apps.tag"
"""
App name end
"""

"""
URL constants
"""
TAG_URL = "tag"
TAG_BASENAME = "tag"
"""
URL constants end
"""

"""
Model constants
"""
TAG_NAME_MAX_LENGTH = 255
TAG_NAME_HELP_TEXT = "Display name of the tag"
TAG_IS_SYSTEM_HELP_TEXT = "Whether this tag is system-managed"
"""
Model constants end
"""
```

### `apps/tag/models.py`
```python
from django.db import models
from apps.core.models import Timestamps
from apps.tag.constants import TAG_IS_SYSTEM_HELP_TEXT, TAG_NAME_HELP_TEXT, TAG_NAME_MAX_LENGTH


class Tag(Timestamps):
    name = models.CharField(max_length=TAG_NAME_MAX_LENGTH, help_text=TAG_NAME_HELP_TEXT)
    is_system = models.BooleanField(default=False, help_text=TAG_IS_SYSTEM_HELP_TEXT)

    class Meta:
        db_table = "tag"
        ordering = ["-created_ts"]

    def __str__(self):
        return self.name
```

### `apps/tag/serializers.py`
```python
from rest_framework.serializers import ModelSerializer
from apps.tag.models import Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
```

### `apps/tag/views.py`
```python
from apps.core.constants import DELETE, GET, PATCH, POST
from apps.core.views import BaseViewset
from apps.tag.models import Tag
from apps.tag.serializers import TagSerializer


class TagViewset(BaseViewset):
    http_method_names = [GET, POST, PATCH, DELETE]
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    ordering = ["-modified_ts"]
```

### `apps/tag/urls.py`
```python
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.tag.constants import TAG_BASENAME, TAG_URL
from apps.tag.views import TagViewset

router = DefaultRouter()
router.register(TAG_URL, TagViewset, basename=TAG_BASENAME)

urlpatterns = [
    path("", include(router.urls)),
]
```

### `apps/tag/apps.py`
```python
from django.apps import AppConfig
from apps.tag.constants import TAG_APP

class TagConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = TAG_APP
```

## Wiring

**1. Add to `PROJECT_APPS` in `settings.py`:**
```python
PROJECT_APPS = [
    "apps.user",
    "apps.product",   # add here
]
```

**2. Include in `<package_name>/urls.py`:**
```python
urlpatterns_v1 = [
    path(V1_API_PREFIX, include("apps.user.urls")),
    path(V1_API_PREFIX, include("apps.product.urls")),   # add here
]
```

**3. Run migrations:**
```bash
python manage.py makemigrations product
python manage.py migrate
```

