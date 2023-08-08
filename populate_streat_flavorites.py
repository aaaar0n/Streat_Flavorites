import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sflavorites.settings")  # Replace "your_project_name" with your project's actual name
django.setup()

from streat_flavorites.models import Category, Subcategory, Item

def populate():
    # Create categories
    category1 = Category.objects.create(name="Category 1")
    category2 = Category.objects.create(name="Category 2")

    # Create subcategories under Category 1
    subcategory1_1 = Subcategory.objects.create(name="Subcategory 1.1", category=category1)
    subcategory1_2 = Subcategory.objects.create(name="Subcategory 1.2", category=category1)

    # Create subcategories under Category 2
    subcategory2_1 = Subcategory.objects.create(name="Subcategory 2.1", category=category2)
    subcategory2_2 = Subcategory.objects.create(name="Subcategory 2.2", category=category2)

    # Create items under Subcategory 1.1
    item1 = Item.objects.create(name="Item 1", description="Description for Item 1", price=10.99, stocks=50, subcategory=subcategory1_1)
    item2 = Item.objects.create(name="Item 2", description="Description for Item 2", price=15.99, stocks=30, subcategory=subcategory1_1)

    # Create items under Subcategory 2.2
    item3 = Item.objects.create(name="Item 3", description="Description for Item 3", price=8.49, stocks=20, subcategory=subcategory2_2)

if __name__ == '__main__':
    populate()
    print("Sample data populated successfully.")
