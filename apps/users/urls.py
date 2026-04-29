from django.urls import path
from .views import (
    SignupView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    ChangePasswordView,
    StaffInviteView,
    StaffListView,
    StaffToggleActiveView,
    ForgotPasswordView,
    ResetPasswordView,
)

app_name = 'users'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('staff/invite/', StaffInviteView.as_view(), name='staff-invite'),
    path('staff/list_staff/', StaffListView.as_view(), name='staff-list'),
    path('staff/<int:pk>/toggle_active/', StaffToggleActiveView.as_view(), name='staff-toggle'),
]
