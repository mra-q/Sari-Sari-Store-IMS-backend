from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.conf import settings
from django.core.cache import cache
import secrets
import os
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    StaffInviteSerializer,
    ChangePasswordSerializer,
    UserSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from .models import User


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            response = Response({
                'message': 'Owner account created successfully',
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_201_CREATED)
            
            # Use secure cookies in production (HTTPS), allow insecure in development
            is_secure = not settings.DEBUG and os.environ.get('DJANGO_ENV') == 'production'
            
            response.set_cookie(
                key='access_token',
                value=str(refresh.access_token),
                httponly=True,
                secure=is_secure,
                samesite='Strict' if is_secure else 'Lax',
                max_age=3600
            )
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=is_secure,
                samesite='Strict' if is_secure else 'Lax',
                max_age=86400
            )
            
            return response
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("Login request data:", request.data)
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            response = Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)
            
            # Use secure cookies in production (HTTPS), allow insecure in development
            is_secure = not settings.DEBUG and os.environ.get('DJANGO_ENV') == 'production'
            
            response.set_cookie(
                key='access_token',
                value=str(refresh.access_token),
                httponly=True,
                secure=is_secure,
                samesite='Strict' if is_secure else 'Lax',
                max_age=3600
            )
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=is_secure,
                samesite='Strict' if is_secure else 'Lax',
                max_age=86400
            )
            
            return response
        print("Login errors:", serializer.errors)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except TokenError:
            pass
        
        response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh') or request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token not found'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            
            # Use secure cookies in production (HTTPS), allow insecure in development
            is_secure = not settings.DEBUG and os.environ.get('DJANGO_ENV') == 'production'
            
            response = Response({
                'message': 'Token refreshed successfully',
                'access': access_token
            }, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=is_secure,
                samesite='Strict' if is_secure else 'Lax',
                max_age=3600
            )
            
            return response
        except TokenError:
            return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if not request.user.check_password(old_password):
            return Response(
                {'error': {'old_password': ['Current password is incorrect.']}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.set_password(new_password)
        request.user.must_change_password = False
        request.user.save(update_fields=['password', 'must_change_password', 'updated_at'])

        return Response(
            {
                'message': 'Password changed successfully',
                'user': UserSerializer(request.user).data,
            },
            status=status.HTTP_200_OK,
        )


class StaffInviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'OWNER':
            return Response({'error': 'Only owners can invite staff'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = StaffInviteSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            user = result['user']
            temp_password = result['temporary_password']
            
            return Response({
                'message': 'Staff invited successfully',
                'credentials': {
                    'email': user.email,
                    'temporary_password': temp_password,
                    'username': user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class StaffListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'OWNER':
            return Response({'error': 'Only owners can view staff list'}, status=status.HTTP_403_FORBIDDEN)
        
        staff_members = User.objects.filter(role='STAFF')
        serializer = UserSerializer(staff_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StaffToggleActiveView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if request.user.role != 'OWNER':
            return Response({'error': 'Only owners can toggle staff status'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            staff = User.objects.get(pk=pk, role='STAFF')
            staff.is_active = not staff.is_active
            staff.save()
            return Response(UserSerializer(staff).data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Staff member not found'}, status=status.HTTP_404_NOT_FOUND)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        reset_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        
        # Store reset code in cache (10 minutes expiry)
        cache.set(f'reset_code_{email}', reset_code, timeout=600)
        
        # TODO: In production, send reset_code via email instead of returning it in response
        # For development/testing, we return it directly
        response_data = {'message': 'Password reset code sent'}
        if settings.DEBUG:
            response_data['reset_code'] = reset_code  # Only expose in development
        
        return Response(response_data, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        reset_code = serializer.validated_data['reset_code']
        new_password = serializer.validated_data['new_password']
        
        cached_code = cache.get(f'reset_code_{email}')
        if not cached_code or cached_code != reset_code:
            return Response({'error': 'Invalid or expired reset code'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            cache.delete(f'reset_code_{email}')
            
            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
