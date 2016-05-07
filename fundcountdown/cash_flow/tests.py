from django.test import TestCase
from moneyed import Money, USD
from fundcountdown.cash_flow.models import Expense, Quotation


class CashOutflowTest(TestCase):

    def setUp(self):
        # Normal Expense
        Expense.objects.create(
            name="Home Rental",
            description="Rent price for home",
            value=Money(150, USD),
            occurrence=6,
            payment_required=True
        )
        # Expense with Quotations
        airfare_expense = Expense.objects.create(
            name="Airfare",
            description="Airfare for travel to place",

        )
        airfare_expense.quotations.create(
            name="Lower Airlines",
            description="Lower price",
            value=Money(1400, USD),
            occurrence=2
        )
        airfare_expense.quotations.create(
            name="Larger Airlines",
            description="Larger price",
            value=Money(2900.50, USD),
            occurrence=1,
            payment_required=False
        )
        market = Expense.objects.create(
            name="Market",
            description="Because we need beer and steak."
        )
        Quotation.objects.create(
            name="Super Market",
            description="Yes! We have beer.",
            value=Money(100.49, USD),
            occurrence=1,
            expense=market
        )

    def test_quotations(self):
        quotation = Quotation.objects.get(name='Larger Airlines')
        self.assertEqual(quotation.value, Money(2900.50, USD))
        self.assertEqual(quotation.amount, Money(2900.50, USD))
        self.assertFalse(quotation.payment_required)

        market = Quotation.objects.get(name='Super Market')
        self.assertFalse(market.is_winner)
        market.is_winner = True
        market.save()
        self.assertTrue(market.is_winner)

    def test_normal_expense(self):
        home_rental = Expense.objects.get(name='Home Rental')
        self.assertEqual(home_rental.__repr__(), 'Home Rental')
        self.assertEqual(home_rental.value, Money(150, USD))
        self.assertEqual(home_rental.amount, Money(900, USD))
        self.assertTrue(home_rental.payment_required)
        # Update values
        home_rental.occurrence = 0
        home_rental.value = 180
        home_rental.save()
        # Occurrence not be less than 1
        self.assertEqual(home_rental.occurrence, 1)
        self.assertEqual(home_rental.amount, Money(180, USD))

    def test_expense_with_quotations(self):
        airfare = Expense.objects.get(name='Airfare')
        self.assertEqual(airfare.value, Money(2800, USD))
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
