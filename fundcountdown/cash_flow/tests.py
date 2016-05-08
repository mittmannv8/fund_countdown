from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from moneyed import USD, BRL, Money
from fundcountdown.cash_flow.models import Account
from fundcountdown.cash_flow.models import CashInput
from fundcountdown.cash_flow.models import Expense
from fundcountdown.cash_flow.models import Quotation
from fundcountdown.cash_flow.models import InputCategory
from fundcountdown.fund.models import Fund


class CashOutflowTest(TestCase):

    def setUp(self):
        due_date = timezone.now()
        travel = Fund.objects.create(
            name="Travel Fund",
            description="Travel around the World",
            expected_date=timezone.datetime(2017, 1, 1, tzinfo=timezone.utc),
        )
        partner = User.objects.create(username='u', password='p')
        # Normal Expense
        Expense.objects.create(
            name="Home Rental",
            description="Rent price for home",
            value=Money(150, USD),
            occurrence=6,
            payment_required=True,
            due_date=due_date,
            fund=travel,
            partner=partner
        )
        # Expense with Quotations
        airfare_expense = Expense.objects.create(
            name="Airfare",
            description="Airfare for travel to place",
            due_date=due_date,
            fund=travel,
            partner=partner

        )
        airfare_expense.quotations.create(
            name="Lower Airlines",
            description="Lower price",
            value=Money(1400, USD),
            occurrence=2,
            due_date=due_date,
            fund=travel,
            partner=partner
        )
        airfare_expense.quotations.create(
            name="Larger Airlines",
            description="Larger price",
            value=Money(2900.50, USD),
            occurrence=1,
            payment_required=False,
            due_date=due_date,
            fund=travel,
            partner=partner
        )
        market = Expense.objects.create(
            name="Market",
            description="Because we need beer and steak.",
            due_date=due_date,
            fund=travel,
            partner=partner
        )
        Quotation.objects.create(
            name="Super Market",
            description="Yes! We have beer.",
            value=Money(100.49, USD),
            occurrence=1,
            expense=market,
            due_date=due_date,
            fund=travel,
            partner=partner
        )

    def test_quotations(self):
        travel = Fund.objects.first()
        quotation = Quotation.objects.get(name='Larger Airlines')
        self.assertEqual(quotation.value, Money(2900.50, USD))
        self.assertEqual(quotation.amount, Money(2900.50, USD))
        self.assertFalse(quotation.payment_required)
        self.assertEqual(quotation.fund, travel)

        market = Quotation.objects.get(name='Super Market')
        self.assertFalse(market.is_winner)
        market.is_winner = True
        market.save()
        self.assertTrue(market.is_winner)

    def test_normal_expense(self):
        travel = Fund.objects.first()
        home_rental = Expense.objects.get(name='Home Rental')
        self.assertEqual(home_rental.__repr__(), 'Home Rental')
        self.assertEqual(home_rental.value, Money(150, USD))
        self.assertEqual(home_rental.amount, Money(900, USD))
        self.assertTrue(home_rental.payment_required)
        self.assertEqual(home_rental.fund, travel)
        # Update values
        home_rental.occurrence = 0
        home_rental.value = 180
        home_rental.save()
        # Occurrence not be less than 1
        self.assertEqual(home_rental.occurrence, 1)
        self.assertEqual(home_rental.amount, Money(180, USD))

    def test_expense_with_quotations(self):
        airfare = Expense.objects.get(name='Airfare')
        self.assertEqual(airfare.value, Money(1400, USD))
        self.assertEqual(airfare.amount, Money(2800, USD))
        self.assertTrue(airfare.has_quotation)

        market = Expense.objects.get(name='Market')
        self.assertEqual(market.amount, Money(100.49, USD))

        # Change winner quotation manually
        airfare_lower, airfare_larger = airfare.quotations.all()
        self.assertEqual(airfare.winner, airfare_lower)
        airfare.winner = airfare_larger
        airfare.save()
        self.assertEqual(airfare.winner, airfare_larger)
        self.assertEqual(airfare.amount, Money(2900.50, USD))

        # Test occurrence, time ever
        # Migrate Expenses to quotation
        # Migrate Quotations to Expense
        # Test priority
        # Expenses can be before and after
        # Insert date


class CashInputTest(TestCase):

    def setUp(self):
        self.input_one_date = timezone.now()
        self.input_two_date = timezone.now()
        travel = Fund.objects.create(
            name="Travel Fund",
            description="Travel around the World",
            expected_date=timezone.datetime(2017, 1, 1, tzinfo=timezone.utc),
        )
        wallet = Account.objects.create(
            name='Wallet',
            description='My wallet',
            fund=travel,
        )
        saving = InputCategory.objects.create(
            name="Saving",
            description="Saving monthly"
        )
        less_fastfood = InputCategory.objects.create(
            name="Less fastfood",
            description="Eat less fastfood"
        )
        cash_input = CashInput.objects.create(
            description='Savings (not eaten thats Burguer King)',
            value=200,
            entry_date=self.input_one_date,
            account=wallet,
        )
        cash_input.category.add(saving, less_fastfood)
        cash_input = CashInput.objects.create(
            description='Not buy the game on Steam',
            value=130,
            entry_date=self.input_one_date,
            account=wallet,
        )
        cash_input.category.add(saving)

    def test_cash_input(self):
        account = Account.objects.first()
        cash_input = CashInput.objects.first()
        self.assertEqual(cash_input.value, Money(200, BRL))
        self.assertEqual(cash_input.account, account)
        self.assertEqual(cash_input.entry_date, self.input_one_date)

    def test_input_category(self):
        category = InputCategory.objects.first()
        self.assertEqual(category.inputs.count(), 2)
        self.assertEqual(category.amount(), Money(330, BRL))


class AccountTest(TestCase):
    def setUp(self):
        travel = Fund.objects.create(
            name="Travel Fund",
            description="Travel around the World",
            expected_date=timezone.datetime(2017, 1, 1, tzinfo=timezone.utc),
        )
        bank_account = Account.objects.create(
            name='Bank Money',
            description='Bank',
            fund=travel
        )
        CashInput.objects.create(
            description='Savings',
            value=100,
            entry_date=timezone.now(),
            account=bank_account
        )
        CashInput.objects.create(
            description='Savings',
            value=122.60,
            entry_date=timezone.now(),
            account=bank_account
        )

    def test_account(self):
        account = Account.objects.first()
        self.assertEqual(account.balance, Money(222.60, BRL))
