import random
from decimal import Decimal
from datetime import date

from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum
from api.models import Books, Order, OrderItem, Product, User

class Command(BaseCommand):
    help = 'Creates application data'

    def handle(self, *args, **kwargs):
        # Keep the command safe to run multiple times by updating known records.
        user = User.objects.filter(username='admin').first()
        if not user:
            user = User.objects.create_superuser(
                username='admin',
                password='test',
                email='admin@example.com',
            )

        demo_users = [
            ('alice', 'alice@example.com', False),
            ('bob', 'bob@example.com', False),
        ]
        for username, email, is_staff in demo_users:
            User.objects.update_or_create(
                username=username,
                defaults={
                    'email': email,
                    'is_staff': is_staff,
                },
            )

        products = [
            {
                'name': "A Scanner Darkly",
                'description': lorem_ipsum.paragraph(),
                'price': Decimal('12.99'),
                'stock': 4,
            },
            {
                'name': "Coffee Machine",
                'description': lorem_ipsum.paragraph(),
                'price': Decimal('70.99'),
                'stock': 6,
            },
            {
                'name': "Velvet Underground & Nico",
                'description': lorem_ipsum.paragraph(),
                'price': Decimal('15.99'),
                'stock': 11,
            },
            {
                'name': "Enter the Wu-Tang (36 Chambers)",
                'description': lorem_ipsum.paragraph(),
                'price': Decimal('17.99'),
                'stock': 2,
            },
            {
                'name': "Digital Camera",
                'description': lorem_ipsum.paragraph(),
                'price': Decimal('350.99'),
                'stock': 4,
            },
            {
                'name': "Watch",
                'description': lorem_ipsum.paragraph(),
                'price': Decimal('500.05'),
                'stock': 0,
            },
        ]

        for product_data in products:
            Product.objects.update_or_create(
                name=product_data['name'],
                defaults=product_data,
            )

        books = [
            ('Atomic Habits', 'James Clear', date(2018, 10, 16)),
            ('Deep Work', 'Cal Newport', date(2016, 1, 5)),
            ('Clean Code', 'Robert C. Martin', date(2008, 8, 1)),
            ('The Pragmatic Programmer', 'Andrew Hunt', date(1999, 10, 30)),
        ]
        for name, author, published in books:
            Books.objects.update_or_create(
                name=name,
                author=author,
                defaults={'published': published},
            )

        existing_orders = Order.objects.filter(user=user).count()
        seeded_products = list(Product.objects.order_by('name'))
        for _ in range(max(0, 3 - existing_orders)):
            order = Order.objects.create(user=user)
            for product in random.sample(seeded_products, 2):
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=random.randint(1, 3),
                )

        self.stdout.write(self.style.SUCCESS('Database populated with demo data.'))
