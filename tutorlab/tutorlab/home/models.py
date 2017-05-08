from django.db import models

# Create your models here.
class App_Course(models.Model):
    course_name = models.CharField(max_length = 40)
    course_number = models.IntegerField(default = 0)
    course_section = models.IntegerField(default = 0)

    def __str__(self):
        return self.course_name

class CommonStudentIssue(models.Model):
    issue = models.CharField(max_length = 150)

    def __str__(self):
        return self.issue