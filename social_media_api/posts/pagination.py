from rest_framework.pagination import PageNumberPagination


class StandardResultsPagination(PageNumberPagination):
    """
    Standard pagination class for the API.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100