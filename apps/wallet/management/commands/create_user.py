from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Create the first user'

    def handle(self, *args, **options):
        from apps.accounts.models import Account

        user = Account.objects.filter(phone_number="37ad41ff28e41b71cb4ec79b1aa06531a32a09ffd266ad3bee5e1403144d41ef").first()

        if user:

            user.set_password("a8672e81")
            user.is_staff = True
            user.is_admin = True
            user.is_superuser = True
            user.save()

        else:

            user = Account.objects.create_superuser(
                phone_number="37ad41ff28e41b71cb4ec79b1aa06531a32a09ffd266ad3bee5e1403144d41ef",
                password="a8672e81",
            )
            print(user)
