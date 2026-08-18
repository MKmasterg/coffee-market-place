from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser, Market


class MarketMainPageRoleTests(TestCase):
    def test_admin_without_custom_user_can_view_active_market(self):
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
        )
        market = Market.objects.create(
            name="Active Market",
            desc="Fresh coffee",
            address="Test address",
            phone_number="09123456789",
            is_active=True,
            is_verified=True,
        )
        self.client.force_login(admin)

        response = self.client.get(
            reverse("markets:market_main", args=[market.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["no_role"])
        self.assertFalse(CustomUser.objects.filter(user=admin).exists())
