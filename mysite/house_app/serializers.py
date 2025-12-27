from rest_framework import serializers
from .models import (UserProfile, Review, Region, City, District, Property, PropertyImage)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'username','age',  'password',  'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }





class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'user_role']

    def get_queryset(self):
        return UserProfile.objects.all(id=self.request.user.id)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']

    def get_queryset(self):
        return UserProfile.objects.all(id=self.request.user.id)


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = [ 'region_name']


class CitySerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = City
        fields = ['city_name','region']


class DistrictSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = District
        fields = [ 'district', 'city']


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['image']

class PropertyListSerializer(serializers.ModelSerializer):
    image = PropertyImageSerializer(read_only=True)
    avg_rating = serializers.FloatField(source='get_avg_rating', read_only=True)
    count_people = serializers.IntegerField(source='get_count_people', read_only=True)
    class Meta:
        model = Property
        fields = ['image', 'title', 'floor', 'property_type', 'avg_rating', 'count_people' ]

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating']


class PropertyDetailSerializer(serializers.ModelSerializer):
    image = PropertyImageSerializer(read_only=True)
    seller = UserProfileSerializer(read_only=True)
    buyer = UserProfileSerializer(read_only=True)
    region = RegionSerializer(read_only=True)
    city = CitySerializer(read_only=True)
    district = DistrictSerializer(read_only=True)
    property_img = PropertyImageSerializer(many=True, read_only=True)
    avg_rating = serializers.FloatField(source='get_avg_rating', read_only=True)
    count_people = serializers.IntegerField(source='get_count_people', read_only=True)
    review = ReviewSerializer(read_only=True)

    class Meta:
        model = Property
        fields = [
            'id','image', 'title', 'description', 'property_type', 'region', 'city', 'district',
            'address', 'area', 'price', 'rooms', 'floor', 'total_floors',
            'documents', 'seller', 'condition',
            'avg_rating', 'count_people'
        ]

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()

class ReviewListSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = Review
        fields =['author', 'seller', 'rating', 'comment']