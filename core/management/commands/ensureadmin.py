from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Ensures the admin superuser exists'

    def add_arguments(self, parser):
        parser.add_argument('password', type=str)
        parser.add_argument('domain', type=str)

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            existing_admin = User.objects.get(username="admin")
        except User.DoesNotExist:
            User.objects.create_superuser('admin', "admin@%s" % options['domain'], options['password'])
