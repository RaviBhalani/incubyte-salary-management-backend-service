from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.core.constants import PAGE_SIZE, MAX_PAGE_SIZE


class ListPagination(PageNumberPagination):
    page_size = PAGE_SIZE
    max_page_size = MAX_PAGE_SIZE
    page_size_query_param = "page_size"

    def paginate_queryset(self, queryset, request, view=None):
        if "page" not in request.query_params:
            return None  # DRF interprets this as "don't paginate"

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            ),        )

