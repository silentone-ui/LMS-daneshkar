from django.contrib.auth.hashers import make_password
from django.core.management import CommandParser
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from accounts.models import User
from users.models import Profile


class Command(BaseCommand):
    help = "creating fake user for database"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--count", type=int, default=5)

    @transaction.atomic
    def handle(self, *args, **option):
        fake = Faker("fa-IR")
        count = option["count"]
        self.stdout.write(f"تعداد{count}یوزر در  حال ساخت است")

        default_password = make_password("test1234hash5678hello")
        users = []
        for _ in range(count):
            users.append(
                User(
                    phone=fake.unique.numerify("09#########"),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    password=default_password,
                )
            )
        create_users = User.objects.bulk_create(users, batch_size=200)
        profiles = []
        for user in create_users:
            profiles.append(
                Profile(
                    user=user,
                    full_name=f"{user.first_name} {user.last_name}".strip(),
                    role=Profile.Role.STUDENT,
                )
            )
        Profile.objects.bulk_create(profiles, batch_size=200)
        self.stdout.write(self.style.SUCCESS("یوزر ها ساخته شدند"))
