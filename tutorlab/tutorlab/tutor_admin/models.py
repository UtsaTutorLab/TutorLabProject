from django.db import models
from datetime import datetime

class Term(models.Model):
    name = models.CharField(max_length=15, null=True)
    start = models.DateField()
    end = models.DateField()

    @classmethod
    def create(cls, name, start, end):
        term = cls(name=name, start=start, end=end)
        return term

    def __str__(self):
        return str(self.name)

    def inTerm(self, date):
        if date >= self.start and date <= self.end:
            return True
        else:
            return False

    def beforeTerm(self, date):
        if date < self.start:
            return True
        else:
            return False

