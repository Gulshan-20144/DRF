from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_query_param = 'page'  # Corrected attribute name
    page_size_query_param='record'
    max_page_size = 100  # Maximum page size

    def paginate_queryset(self, queryset, request, view=None):
        if request is not None:
            if bool(request.query_params.get('all')) == True:
                return None
        return super( ).paginate_queryset(queryset, request, view)
    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })