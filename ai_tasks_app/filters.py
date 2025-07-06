import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__id")
    status = django_filters.CharFilter(lookup_expr='iexact')
    priority = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Task
        fields = ['category', 'status', 'priority']
