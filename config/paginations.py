from rest_framework.pagination import PageNumberPagination


class ResultsSetPagination(PageNumberPagination):
    page_size = 40
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def set_page_size(self, size):
        self.page_size = size
    
    def set_max_page_size(self, size):
        self.max_page_size = size