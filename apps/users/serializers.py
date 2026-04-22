from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'phone', 
                  'password', 'store_name', 'store_address']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        validated_data['role'] = 'OWNER'
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required")

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        data['user'] = user
        return data


class StaffInviteSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20)
    temporary_password = serializers.CharField(min_length=6, required=False)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        import secrets
        import string
        
        full_name = validated_data['full_name']
        name_parts = full_name.split()
        first_name = name_parts[0]
        last_name = name_parts[-1] if len(name_parts) > 1 else ''
        middle_name = ' '.join(name_parts[1:-1]) if len(name_parts) > 2 else ''

        temp_password = validated_data.get('temporary_password')
        if not temp_password:
            chars = string.ascii_letters + string.digits
            temp_password = ''.join(secrets.choice(chars) for _ in range(10))

        user = User.objects.create_user(
            email=validated_data['email'],
            password=temp_password,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            phone=validated_data['phone_number'],
            role='STAFF',
            is_active=True,
            must_change_password=True,
        )

        return {
            'user': user,
            'temporary_password': temp_password
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')

        if old_password == new_password:
            raise serializers.ValidationError(
                {'new_password': ['New password must be different from the current password.']}
            )

        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'middle_name', 'last_name', 
                  'phone', 'role', 'store_name', 'store_address', 'is_active', 'must_change_password']
