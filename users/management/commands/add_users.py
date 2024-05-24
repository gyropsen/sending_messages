from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = Group.objects.get(name="users")
        moderators = Group.objects.get(name="moderators")

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

        moderator = User.objects.create(
            email="moderator@gmail.com",
            first_name="moderator",
            last_name="moderator",
            is_superuser=False,
            is_staff=True,
            is_active=True,
        )

        user1.set_password("12345")
        user2.set_password("12345")
        moderator.set_password("12345")

        users.user_set.add(user1)
        users.user_set.add(user2)
        moderators.user_set.add(moderator)

        user1.save()
        user2.save()
        moderator.save()
