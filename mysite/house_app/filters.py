from django_filters import FilterSet
from .models import Property


class PropertyListFilter(FilterSet):
    class Meta:
        model = Property
        fields = {
            'region': ['exact'],
            'city': ['exact'],
            'district': ['exact'],
            'property_type': ['exact'],
            'price': ['gte', 'lte'],
            'area': ['gte', 'lte'],
            'rooms': ['exact'],
            'floor': ['exact'],
            'condition': ['exact'],
            'from_owner': ['exact'],
            'has_documents': ['exact'],
        }
