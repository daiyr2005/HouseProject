from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

class Region(models.Model):
    region_name = models.CharField(max_length=70)

    def __str__(self):
        return self.region_name

class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=30)

    def __str__(self):
        return self.city_name


class District(models.Model):
    city = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.CharField(max_length=30)

    def __str__(self):
        return self.district



class Property(models.Model):
    CONDITION_CHOICES = (
        ('new', 'New'),
        ('good', 'Good'),
        ('needs_repair', 'Needs repair'),
    )

    PROPERTY_TYPES= (
        ('apartment', 'Квартира'),
        ('house', 'Дом'),
        ('land', 'Участок'),
        ('commercial', 'Коммерческая недвижимость'),
    )


    title = models.CharField(max_length=255)
    description = models.TextField()  # многоязычность можно реализовать через django-parler или отдельные таблицы
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=255)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    rooms = models.IntegerField()
    floor = models.PositiveIntegerField()
    total_floors = models.PositiveIntegerField()

    documents = models.FileField(upload_to='property_docs/', blank=True, null=True)
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='properties')
    condition = models.CharField( max_length=20,choices=CONDITION_CHOICES )


    def __str__(self):
        return f'{self.title}, {self.city}'



    def get_avg_rating(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return round(sum([i.stars for i in ratings ]) / ratings.count(), 1)
        return 0

    def get_count_people(self):
        return self.reviews.count()

class PropertyImage(models.Model):
    image = models.ImageField(upload_to='property_images/')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_img')

    def __str__(self):
        return f'{self.property}, {self.image}'



class Review(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews_written')
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews_received')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self):
        return f'{self.author}, {self.seller}'
    

