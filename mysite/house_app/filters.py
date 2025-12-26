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
            'price': ['gt', 'lt'],
            'area': ['gt', 'lt'],
            'rooms': ['exact'],
            'floor': ['exact'],
            'condition': ['exact'],
            'seller': ['exact'],
        }
