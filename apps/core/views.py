from rest_framework.filters import OrderingFilter
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from rest_framework.viewsets import GenericViewSet

from apps.core.custom_exception_handlers import get_response
from apps.core.pagination import ListPagination


class BaseListModelMixin(ListModelMixin):

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return get_response(data=response.data, success=True)


class BaseRetrieveModelMixin(RetrieveModelMixin):

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return get_response(
            data=response.data,
            success=True,
        )


class BaseCreateModelMixin(CreateModelMixin):

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return get_response(
            data=response.data,
            resource_created=True,
            headers=response.headers,
        )


class BaseUpdateModelMixin(UpdateModelMixin):

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return get_response(response.data, success=True)


class BaseDestroyModelMixin(DestroyModelMixin):

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return get_response(data=response.data, no_content=True)
    

class BaseOrderingFilterMixin:
    filter_backends = (OrderingFilter,)
    ordering_fields = ['id',]
    ordering = ['-id']


class BaseViewset(
    BaseOrderingFilterMixin,
    BaseListModelMixin,
    BaseCreateModelMixin,
    BaseRetrieveModelMixin,
    BaseUpdateModelMixin,
    BaseDestroyModelMixin,
    GenericViewSet
):
    pagination_class = ListPagination