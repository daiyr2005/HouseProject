from rest_framework.pagination import PageNumberPagination

class PropertyListPagination(PageNumberPagination):
    page_size = 4