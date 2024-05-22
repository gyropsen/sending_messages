from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user1 = User.objects.create(
            email="user1@gmail.com",
            first_name="user1",
            last_name="user1",
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )

        user2 = User.objects.create(
            email="user2@gmail.com",
            first_name="user2",
            last_name="user2",
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )

        user1.set_password("12345")
        user2.set_password("12345")
        user1.save()
        user2.save()
