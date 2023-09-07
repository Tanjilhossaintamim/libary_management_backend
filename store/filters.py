from django_filters import FilterSet
from store.models import Book


class CustomFilter(FilterSet):
    class Meta:
        model = Book
        fields = ['category']
