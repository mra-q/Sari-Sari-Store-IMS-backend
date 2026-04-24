from django.urls import path
from .views import SyncView, SyncPullView

urlpatterns = [
    path('', SyncView.as_view(), name='sync'),
    path('pull/', SyncPullView.as_view(), name='sync-pull'),
]
