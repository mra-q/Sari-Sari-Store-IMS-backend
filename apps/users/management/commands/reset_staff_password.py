from django.core.management.base import BaseCommand
from apps.users.models import User


class Command(BaseCommand):
    help = 'Reset staff password'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Staff email')
        parser.add_argument('password', type=str, help='New password')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Password reset for {email}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {email} not found'))
