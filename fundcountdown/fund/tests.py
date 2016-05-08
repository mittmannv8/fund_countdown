from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from moneyed import Money, USD, BRL
from fundcountdown.cash_flow.models import Account
from fundcountdown.cash_flow.models import CashInput
from fundcountdown.cash_flow.models import Expense
from fundcountdown.fund.models import Fund


class FundTest(TestCase):

    def setUp(self):
        partner1 = User.objects.create(username='p1', password='p')
        partner2 = User.objects.create(username='p2', password='p')
        date = timezone.now()
        travel = Fund.objects.create(
            name="Travel Fund",
            description="Travel around the World",
            expected_date=timezone.datetime(2017, 1, 1, tzinfo=timezone.utc),
        )
        travel.partners.add(partner1, partner2)

        Expense.objects.create(
            name="Home Rental",
            description="Rent price for home",
            value=Money(150, USD),
            occurrence=6,
            payment_required=True,
            due_date=date,
            fund=travel,
            partner=partner1
        )
        # Expense with Quotations
        airfare_expense = Expense.objects.create(
            name="Airfare",
            description="Airfare for travel to place",
            due_date=date,
            fund=travel,
            partner=partner1

        )
        airfare_expense.quotations.create(
            name="Lower Airlines",
            description="Lower price",
            value=Money(1400, USD),
            occurrence=2,
            due_date=date,
            fund=travel,
            partner=partner1
        )
        airfare_expense.quotations.create(
            name="Lower Airlines",
            description="Lower price",
            value=Money(3400, USD),
            occurrence=2,
            due_date=date,
            fund=travel,
            partner=partner1
        )
        # Inputs
        wallet = Account.objects.create(
            name='Wallet',
            description='My wallet',
            fund=travel
        )
        CashInput.objects.create(
            description='Savings',
            value=200,
            entry_date=date,
            account=wallet
        )
        CashInput.objects.create(
            description='Savings',
            value=150,
            entry_date=date,
            account=wallet
        )

    def test_fund(self):
        partner1 = User.objects.get(username='p1')
        partner2 = User.objects.get(username='p2')
        travel = Fund.objects.first()
        self.assertEqual(travel.name, "Travel Fund")
        self.assertEqual(travel.expected_date.year, 2017)
        self.assertEqual(travel.partners.first(), partner1)
        self.assertEqual(partner2.funds.first(), travel)

        self.assertEqual(travel.full_cost, Money(3700, USD))
        self.assertEqual(travel.amount, Money(350, BRL))
