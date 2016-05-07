from __future__ import unicode_literals
from django.db import models

from djmoney.models.fields import MoneyField


class ExpenseAbstract(models.Model):
    """ AbstractClass ExpenseAbstract

    Abstract Class that represents a model of spending is to
    set spending or quotation.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    payment_required = models.BooleanField(default=True)
    _fixed_value = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        blank=True,
        null=True,
        default=0
    )
    _amount_value = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        blank=True,
        null=True,
        default=0
    )
    occurrence = models.IntegerField(default=1)

    @property
    def amount(self):
        return self._amount_value

    def save(self, *args, **kwargs):
        # Occurrence not be less than 1
        if self.occurrence < 1:
            self.occurrence = 1
        self._amount_value = self._fixed_value * self.occurrence

        super(ExpenseAbstract, self).save(*args, **kwargs)

    def __repr__(self):
        return self.name

    class Meta:
        abstract = True


class Expense(ExpenseAbstract):
    """ Class Expense

    Extends the abstract class Abstract Expense and represents expenses
    to meet the goal
    It may be an expense already specified or can be an expense with quotations
    """
    @property
    def has_quotation(self):
        if self.quotations.count() > 0:
            return True
        return False

    @property
    def value(self):
        if self.has_quotation:
            return self.winner.value
        else:
            return self._fixed_value

    @value.setter
    def value(self, value):
        if self.has_quotation:
            return NotImplementedError
        else:
            try:
                self._fixed_value = value
            except ValueError:
                raise ValueError(
                    "[{}] isn't a valid Money number.".format(value)
                )
            except:
                raise Exception("An error has occurred.")

    @property
    def winner(self):
        if self.has_quotation:
            return self.quotations.winner()
        else:
            return self

    @winner.setter
    def winner(self, quotation):
        if self.has_quotation:
            quotation.is_winner = True
            quotation.save()
        else:
            return NotImplementedError

    @property
    def amount(self):
        if self.has_quotation:
            return self.winner.amount
        else:
            return self._amount_value

    def __srt__(self):
        return self.name


class QuotationQuerySet(models.QuerySet):
    def winner(self):
        tagget_as_winner = self.filter(is_winner=True)
        if tagget_as_winner.count():
            return tagget_as_winner.first()
        return self.order_by('_amount_value').first()


class Quotation(ExpenseAbstract):
    """ Class Quotation

    Extends the abstract class Abstract Expense and represents
    quotations.
    """
    is_winner = models.BooleanField(default=False)
    expense = models.ForeignKey(Expense, related_name='quotations')

    objects = QuotationQuerySet().as_manager()

    @property
    def has_quotation(self):
        return False

    @property
    def value(self):
        return self._fixed_value

    @value.setter
    def value(self, value):
        try:
            self._fixed_value = value
        except ValueError:
            raise ValueError(
                "[{}] isn't a valid Money number.".format(value)
            )
        except:
            raise Exception("An error has occurred.")

    def save(self, disqualify_winner=False, *args, **kwargs):
        is_disqualify_winner = kwargs.get('disqualify_winner')
        if self.id and self.is_winner and not is_disqualify_winner:
            old_winner = Quotation.objects.winner()
            old_winner.is_winner = False
            old_winner.save(disqualify_winner=True)

        super(Quotation, self).save(*args, **kwargs)

    def __str__(self):
        return "{} [{}]".format(self.name, self.expense.name)
