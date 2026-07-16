from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from users.models import CustomUser, Customer, Market, Order, Seller, Stock

DEMO_PASSWORD = "demo1234"


def create_user(username, email, first_name, last_name, phone, id_number):
    user = User.objects.create_user(
        username=username,
        email=email,
        password=DEMO_PASSWORD,
        first_name=first_name,
        last_name=last_name,
    )
    custom = CustomUser.objects.create(
        user=user,
        phone_number=phone,
        id_number=id_number,
        date_joined=timezone.now(),
    )
    return user, custom


class Command(BaseCommand):
    help = "Seed demo data for local development"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing demo data before seeding",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing data…")
            Order.objects.all().delete()
            Stock.objects.all().delete()
            Seller.objects.all().delete()
            Customer.objects.all().delete()
            Market.objects.all().delete()
            CustomUser.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        if Market.objects.exists():
            self.stdout.write(self.style.WARNING("Data already exists. Use --clear to reseed."))
            return

        now = timezone.now()

        _, seller1_cu = create_user(
            "aria_roast", "aria@coffee.demo", "Aria", "Chen",
            "09121234567", "1234567890",
        )
        _, seller2_cu = create_user(
            "milo_bean", "milo@coffee.demo", "Milo", "Okonkwo",
            "09129876543", "2345678901",
        )
        _, customer_cu = create_user(
            "sam_brew", "sam@coffee.demo", "Sam", "Rivera",
            "09131112222", "3456789012",
        )

        bean_brew = Market.objects.create(
            name="Bean & Brew Co.",
            desc="Small-batch roastery with single-origin highlights",
            address="42 Roastery Lane, Portland",
            phone_number="02144556677",
            rate=5,
            number_of_orders=12,
            is_active=True,
            is_verified=True,
        )
        morning = Market.objects.create(
            name="Morning Ritual",
            desc="Neighborhood café beans — smooth everyday blends",
            address="8 Sunrise Ave, Seattle",
            phone_number="02177889900",
            rate=4,
            number_of_orders=7,
            is_active=True,
            is_verified=True,
        )
        ember = Market.objects.create(
            name="Ember Roast House",
            desc="Dark roasts and espresso-forward profiles",
            address="15 Kiln Street, Austin",
            phone_number="02133445566",
            rate=5,
            number_of_orders=19,
            is_active=True,
            is_verified=True,
        )

        seller1 = Seller.objects.create(user=seller1_cu)
        seller1.markets.add(bean_brew, morning)
        seller1.supervisor.add(bean_brew)

        seller2 = Seller.objects.create(user=seller2_cu)
        seller2.markets.add(ember)
        seller2.supervisor.add(ember)

        stocks_data = [
            (bean_brew, "Ethiopian Yirgacheffe", "Floral, bergamot, light body", 250, True, "0.18"),
            (bean_brew, "Colombian Supremo", "Caramel, red apple, balanced", 180, True, "0.14"),
            (bean_brew, "Guatemala Huehuetenango", "Chocolate, honey, medium roast", 120, True, "0.16"),
            (morning, "House Blend", "Nutty, smooth, all-day drinker", 300, True, "0.11"),
            (morning, "Decaf Swiss Water", "Mellow cocoa, zero caffeine", 90, True, "0.13"),
            (ember, "Italian Espresso", "Bold, crema-rich, dark roast", 200, True, "0.15"),
            (ember, "French Roast", "Smoky, intense, low acidity", 150, True, "0.12"),
            (ember, "Sumatra Mandheling", "Earthy, full body, spice notes", 80, True, "0.17"),
        ]

        stocks = []
        for market, name, desc, qty, available, ppg in stocks_data:
            stocks.append(
                Stock.objects.create(
                    name=name,
                    desc=desc,
                    no=qty,
                    is_available=available,
                    market=market,
                    ppg=ppg,
                )
            )

        customer = Customer.objects.create(
            user=customer_cu,
            home_address="77 Maple Court, Apt 4B, Chicago",
        )
        customer.basket.add(stocks[0], stocks[5])

        Order.objects.create(
            stock=stocks[1],
            customer=customer,
            market=bean_brew,
            number_of_stock=2,
            date_placed=now - timedelta(days=2),
            status=Order.Status.DELIVERED,
            message="Medium grind please, thanks!",
        )
        Order.objects.create(
            stock=stocks[4],
            customer=customer,
            market=morning,
            number_of_stock=1,
            date_placed=now - timedelta(hours=6),
            status=Order.Status.PENDING,
            message="Leave at door if not home.",
        )
        Order.objects.create(
            stock=stocks[6],
            customer=customer,
            market=ember,
            number_of_stock=3,
            date_placed=now - timedelta(days=5),
            status=Order.Status.DECLINED,
            message="Whole bean, coarse grind.",
        )

        self.stdout.write(self.style.SUCCESS("Demo data seeded."))
        self.stdout.write("")
        self.stdout.write("Accounts (password: demo1234):")
        self.stdout.write("  aria_roast  — seller (Bean & Brew, Morning Ritual)")
        self.stdout.write("  milo_bean   — seller (Ember Roast House)")
        self.stdout.write("  sam_brew    — customer (basket has 2 items)")
