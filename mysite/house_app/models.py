from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    ROLE_CHOICES = (
        ('seller', 'seller'),
        ('buyer', 'buyer')
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

class Region(models.Model):
    region_name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.region_name

class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city_image = models.ImageField(upload_to='city_image/')
    city_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.city_name


class District(models.Model):
    city = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.CharField(max_length=30)

    def __str__(self):
        return {self.district}


class Property(models.Model):
    CONDITION_CHOICES = (
        ('new', 'new'),
        ('good', 'good'),
        ('needs_repair', 'needs repair'))
    PROPERTY_TYPES = (
        ('apartment', 'apartment'),
        ('house', 'house'),
        ('land', 'land'))
    title = models.CharField(max_length=100)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='property')
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    area = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.IntegerField()
    floor = models.PositiveIntegerField()
    total_floors = models.PositiveIntegerField()
    documents = models.FileField(upload_to='property_docs/', blank=True, null=True)
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='properties')
    condition = models.CharField( max_length=20,choices=CONDITION_CHOICES )


    def __str__(self):
        return f"{self.title}, {self.city}"



class PropertyImage(models.Model):
    image = models.ImageField(upload_to='property_images/')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.property}, {self.image}'



class Review(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i))for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self):
        return f"{self.author}, {self.seller}"