from django.core.management.base import BaseCommand
from apps.users.models import User
from apps.users.serializers import UserSerializer

class Command(BaseCommand):
    help = 'Test staff user is_active status'

    def handle(self, *args, **options):
        # Get all staff users
        staff_users = User.objects.filter(role='STAFF')
        self.stdout.write(f"\nFound {staff_users.count()} staff users\n")
        
        for user in staff_users:
            self.stdout.write(f"\nStaff: {user.email}")
            self.stdout.write(f"  - Name: {user.first_name} {user.last_name}")
            self.stdout.write(f"  - is_active (model): {user.is_active}")
            
            # Test serialization
            serializer = UserSerializer(user)
            data = serializer.data
            self.stdout.write(f"  - is_active (serialized): {data.get('is_active', 'NOT FOUND')}")
            
            if user.is_active:
                self.stdout.write(self.style.SUCCESS("  [ACTIVE]"))
            else:
                self.stdout.write(self.style.WARNING("  [INACTIVE]"))
        
        self.stdout.write(self.style.SUCCESS('\nTest complete'))
