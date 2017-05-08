from django.db import models
from django.contrib.auth.models import User
from student.models import Student
from home.models import CommonStudentIssue

class Instructor(models.Model):   
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True) 
    first_name = models.CharField(max_length=30)    
    last_name = models.CharField(max_length=30)    
    email = models.EmailField()
    token = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Course(models.Model):
    course_num = models.CharField(max_length=8, default="N/A")
    course_name = models.CharField(max_length = 200, default="N/A")
    Instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.course_num + " " + self.course_name

class Student(models.Model):
    courses = models.ManyToManyField(Course)
    studentID = models.CharField(max_length=6)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.first_name + " " + self.last_name

class CustomIssueSet(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issue = models.ForeignKey(CommonStudentIssue, on_delete=models.CASCADE)
    # issue = models.CharField(max_length=150)

    def __str__(self):
        return str(self.course) + " " + str(self.issue)