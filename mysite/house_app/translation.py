from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(UserProfile)
class UserProfileTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name')


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('city_name',)

@register(Region)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('region_name',)


@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ('district',)

@register(Property)
class PropertyTranslationOptions(TranslationOptions):
    fields = ('district_name','street','condition','property_type', 'description', 'condition')


@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('comment',)