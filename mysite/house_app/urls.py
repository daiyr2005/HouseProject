from django.urls import path, include
from rest_framework import routers
from .views import (RegisterView, LoginView, LogoutView, UserProfileListAPIView,
                    UserProfileAPIView, RegionView, CityView, DistrictView,
                    PropertyListAPIView, PropertyDetailAPIView, PropertyImageView,
                    ReviewAPIView, ReviewListAPIView)

router = routers.DefaultRouter()

router.register('region', RegionView )
router.register('city', CityView)
router.register('district', DistrictView)
router.register('property_image', PropertyImageView)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileListAPIView.as_view(), name='profile'),
    path('profile/<int:pk>/', UserProfileAPIView.as_view(), name='profile'),
    path('property/', PropertyListAPIView.as_view(), name='property_list'),
    path('property/<int:pk>/', PropertyDetailAPIView.as_view(), name='property_detail'),
    path('review/', ReviewAPIView.as_view(), name='review'),
    path('review/<int:pk>/', ReviewListAPIView.as_view(), name='review_list'),
]