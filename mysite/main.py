import os
import django
import random
from decimal import Decimal
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from house_app.models import (
    UserProfile,
    Region,
    City,
    District,
    Property,
    PropertyImage,
    Review
)


def clear_data():
    print("Очистка базы...")
    Review.objects.all().delete()
    PropertyImage.objects.all().delete()
    Property.objects.all().delete()
    District.objects.all().delete()
    City.objects.all().delete()
    Region.objects.all().delete()
    UserProfile.objects.all().delete()
    print("База очищена ✅")


def populate_regions():
    regions_names = [
        "Chui",
        "Osh",
        "Issyk-Kul",
        "Jalal-Abad"
    ]

    regions = []
    for name in regions_names:
        regions.append(Region.objects.create(region_name=name))

    print(f"Регионы: {len(regions)}")
    return regions


def populate_cities(regions):
    cities_data = {
        "Chui": ["Bishkek", "Tokmok"],
        "Osh": ["Osh"],
        "Issyk-Kul": ["Karakol", "Balykchy"],
        "Jalal-Abad": ["Jalal-Abad"]
    }

    cities = []
    for region in regions:
        for city_name in cities_data.get(region.region_name, []):
            cities.append(
                City.objects.create(
                    region=region,
                    city_name=city_name
                )
            )

    print(f"Города: {len(cities)}")
    return cities


def populate_districts(regions):
    districts = []
    for region in regions:
        for i in range(3):
            districts.append(
                District.objects.create(
                    city=region,  # ⚠️ по твоей модели
                    district=f"District {i+1} ({region.region_name})"
                )
            )

    print(f"Районы: {len(districts)}")
    return districts


def populate_users():
    users_data = [
        ("admin", "Admin", "User", "admin"),
        ("seller1", "Ivan", "Petrov", "seller"),
        ("seller2", "Anna", "Ivanova", "seller"),
        ("buyer1", "John", "Smith", "buyer"),
        ("buyer2", "Emma", "Brown", "buyer"),
    ]

    users = []
    for username, first, last, role in users_data:
        users.append(
            UserProfile.objects.create(
                username=username,
                first_name=first,
                last_name=last,
                role=role,
                password=make_password("123456"),
                email=f"{username}@mail.com"
            )
        )

    print(f"Пользователи: {len(users)}")
    return users


def populate_properties(users, regions, cities, districts):
    sellers = [u for u in users if u.role == "seller"]

    properties = []
    for i in range(10):
        property_obj = Property.objects.create(
            title=f"Property {i+1}",
            description="Хорошая недвижимость в удобном районе.",
            property_type=random.choice(["apartment", "house", "land", "commercial"]),
            region=random.choice(regions),
            city=random.choice(cities),
            district=random.choice(districts),
            address=f"Street {i+1}",
            area=Decimal(random.randint(40, 200)),
            price=Decimal(random.randint(30000, 150000)),
            rooms=random.randint(1, 6),
            floor=random.randint(1, 9),
            total_floors=9,
            seller=random.choice(sellers),
            condition=random.choice(["new", "good", "needs_repair"])
        )
        properties.append(property_obj)

    print(f"Недвижимость: {len(properties)}")
    return properties


def populate_property_images(properties):
    images = []
    for prop in properties:
        for i in range(3):
            images.append(
                PropertyImage.objects.create(
                    property=prop,
                    image=f"property_images/property_{prop.id}_{i+1}.jpg"
                )
            )

    print(f"Изображения: {len(images)}")


def populate_reviews(users, properties):
    buyers = [u for u in users if u.role == "buyer"]
    reviews = []

    for prop in properties:
        for _ in range(2):
            buyer = random.choice(buyers)
            reviews.append(
                Review.objects.create(
                    author=buyer,
                    seller=prop.seller,
                    property=prop,
                    rating=random.randint(3, 5),
                    comment="Отличный продавец, всё понравилось!"
                )
            )

    print(f"Отзывы: {len(reviews)}")


def main():
    print("START POPULATE")
    clear_data()
    regions = populate_regions()
    cities = populate_cities(regions)
    districts = populate_districts(regions)
    users = populate_users()
    properties = populate_properties(users, regions, cities, districts)
    populate_property_images(properties)
    populate_reviews(users, properties)
    print("ГОТОВО 🚀")


if __name__ == "__main__":
    main()
