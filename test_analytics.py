"""
Test script for analytics endpoint
Run with: python manage.py shell < test_analytics.py
"""

from apps.stock.views import analytics_view
from django.test import RequestFactory
from django.contrib.auth import get_user_model

User = get_user_model()

# Create a test request
factory = RequestFactory()
request = factory.get('/api/stock/analytics/?period=monthly')

# Get or create a test user
user, _ = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
request.user = user

# Call the view
response = analytics_view(request)

print("Status Code:", response.status_code)
print("Response Data:", response.data)
