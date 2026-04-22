# Inventory-backend/services/staff_service.py

from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class StaffService:
    @staticmethod
    @transaction.atomic
    def create_staff(full_name, email, phone_number, temp_password):
        """
        Create a new staff member with temporary password.
        """
        username = email.split('@')[0]
        base_username = username
        counter = 1
        
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=temp_password,
            full_name=full_name,
            phone_number=phone_number,
            phone=phone_number,
            role='staff',
            is_temp_password=True,
            is_active=True
        )
        
        return user
    
    @staticmethod
    def get_all_staff():
        """
        Get all staff members.
        """
        return User.objects.filter(role='staff').order_by('-created_at')
    
    @staticmethod
    def toggle_staff_status(staff_id):
        """
        Toggle staff active status.
        """
        try:
            staff = User.objects.get(id=staff_id, role='staff')
            staff.is_active = not staff.is_active
            staff.save()
            return staff
        except User.DoesNotExist:
            return None
