from django.contrib.auth.models import User
from django.db import models

# create class model with relation to student


class Student(models.Model):
	student = models.OneToOneField(User, null=True)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	abc123 = models.CharField(max_length=6)
	token = models.CharField(max_length=100, null=True)
	forum_flag_count = models.IntegerField(default=0)

	def __str__(self):
		return str(self.student)


class Queue(models.Model):
	abc123 = models.CharField(max_length = 6)
	whole_name = models.CharField(max_length = 30, null=True)
	chair = models.CharField(max_length = 12)
	className = models.CharField(max_length = 40, null=True)
	classID = models.CharField(max_length = 8)
	question =  models.CharField(max_length = 100, null=True)
	inSession = models.BooleanField(default=False)
	host = models.CharField(max_length=150, null=True)
	port = models.IntegerField(default=0)
	isChat = models.BooleanField(default=0)
	chat_token = models.CharField(max_length=150, null=True)
	def __str__(self):
		return self.abc123
