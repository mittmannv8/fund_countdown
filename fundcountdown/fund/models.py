import operator
from functools import reduce
from django.db import models
from django.contrib.auth.models import User


class Fund(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    expected_date = models.DateField(blank=True, null=True)
    partners = models.ManyToManyField(User, related_name='funds')

    @property
    def full_cost(self):
        expenses = self.expenses.all()
        amount = reduce(operator.add, [e.amount for e in expenses])
        return amount

    @property
    def amount(self):
        inputs = self.accounts.all()
        amount = reduce(operator.add, [i.balance for i in inputs])
        return amount

    def __str__(self):
        return self.name
