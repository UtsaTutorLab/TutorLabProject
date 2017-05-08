from django.db import models
from ta_tutor.models import Tutor
import datetime

class Survey(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True)
    student = models.CharField(max_length = 6, null=True)
    ans1 = models.CharField(max_length = 250)
    ans2 = models.CharField(max_length = 250)
    ans3 = models.CharField(max_length = 250)
    ans4 = models.CharField(max_length = 250)
    ans5 = models.CharField(max_length = 250)
    comment = models.TextField(null=True, blank=True)
    score = models.IntegerField(default=0)
    date_completed = models.DateTimeField(auto_now=True, auto_now_add=False) #will set datetime when updated
    token = models.CharField(max_length=150, null=True)

    def __str__(self):
        return str(self.tutor)

class Choice(models.Model):
    low = models.CharField(max_length=25)
    high = models.CharField(max_length=25)

    def __str__(self):
        return self.low + " to " + self.high

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    scale_choice = models.ForeignKey(Choice)

    def __str__(self):
        return self.question_text


