from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import CustomUser, Market, Seller


class AdminRoleEnrollmentTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
        )
        self.client.force_login(self.admin)

    def test_admin_can_join_as_seller_without_existing_custom_user(self):
        response = self.client.get(reverse("users:seller_sign_up"))

        self.assertRedirects(response, reverse("main"))
        profile = CustomUser.objects.get(user=self.admin)
        self.assertTrue(Seller.objects.filter(user=profile).exists())

    def test_joining_as_seller_twice_is_idempotent(self):
        self.client.get(reverse("users:seller_sign_up"))

        response = self.client.get(reverse("users:seller_sign_up"))

        self.assertRedirects(response, reverse("main"))
        self.assertEqual(CustomUser.objects.filter(user=self.admin).count(), 1)
        self.assertEqual(Seller.objects.filter(user__user=self.admin).count(), 1)

    def test_admin_without_profile_can_open_create_market_form(self):
        response = self.client.get(reverse("users:create_market"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/createMarket.html")
        self.assertFalse(CustomUser.objects.filter(user=self.admin).exists())

    def test_admin_without_role_can_create_market(self):
        response = self.client.post(
            reverse("users:create_market"),
            {
                "name": "Admin Market",
                "desc": "Fresh coffee",
                "address": "Test address",
                "phone_number": "09123456789",
                "is_active": "on",
            },
        )

        self.assertRedirects(response, reverse("main"))
        profile = CustomUser.objects.get(user=self.admin)
        seller = Seller.objects.get(user=profile)
        market = Market.objects.get(name="Admin Market")
        self.assertIn(market, seller.markets.all())
        self.assertIn(market, seller.supervisor.all())
