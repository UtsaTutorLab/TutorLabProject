from django.contrib import admin
from instructor.models import Student, Instructor, Course, CustomIssueSet

admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(CustomIssueSet)
