from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import MSMEProfile, BuyerProfile, LenderProfile

User = get_user_model()

class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            user_type='MSME'
        )

    def test_msme_profile_creation(self):
        profile = MSMEProfile.objects.create(
            user=self.user,
            business_name='Test Business',
            industry_sector='Manufacturing',
            annual_turnover=5000000,
            employee_count=10
        )
        self.assertEqual(str(profile), 'Test Business')

class ViewTests(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')