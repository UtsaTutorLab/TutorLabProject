from django.contrib.auth.models import User
from django.db import models
from student.models import Student

class Tutor(models.Model):
    TUTOR_TYPES = (
        ('CS', 'CS'),
        ('MATLAB', 'MATLAB'),
        ('BOTH', 'BOTH')
    )

    tutor = models.OneToOneField(User, on_delete=models.CASCADE, null=True, limit_choices_to={'groups__name':'TA/Tutors'})
    name = models.CharField(max_length=30, null=True)
    profile_image = models.ImageField(null=True, blank=True)
    classification = models.CharField(max_length=10, default='Freshman')
    about_me = models.TextField(blank=True)
    tutor_type = models.CharField(max_length=6, default='CS', choices=TUTOR_TYPES)
    avg_survey_score = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    survey_count = models.IntegerField(default=0)
    token = models.CharField(max_length=150, null=True)

    @classmethod
    def create(cls, user):
        tutor = cls(tutor=user)
        return tutor

    def __str__(self):
        return str(self.tutor.get_full_name())
    
class Session(models.Model):    
    tutor = models.ForeignKey(Tutor, null=True)
    sessionID = models.DateTimeField(auto_now=False, auto_now_add=True, null=True) #this will set datetime when updated
    student = models.CharField(max_length=6)    
    whole_name = models.CharField(max_length=30, null=True)
    classID = models.CharField(max_length = 40)    
    duration = models.DurationField(max_length=6)    
    notes = models.TextField(help_text='Take detailed notes as you help out.')    
    def __str__(self):        
        return str(self.tutor)

class Notification(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True)
    send_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    message_title = models.CharField(max_length=100)
    message_content = models.CharField(max_length=2000)
    viewed = models.BooleanField(default=False)
    
    @classmethod
    def create(cls, user):
        tutor = cls(tutor=user)
        return tutor

    def __str__(self):
        return self.message_title

class Event(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    start = models.CharField(max_length=50)
    end = models.CharField(max_length=50)
    course = models.CharField(max_length = 40)
    description = models.CharField(max_length=500)
    confirmed = models.BooleanField(default=True)

    @classmethod
    def create(cls, user):
        tutor = cls(tutor=user)
        return tutor

    def __str__(self):
        return str(self.student)
    
class ApptDate(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)    
    course_number = models.CharField(max_length = 40)
    appt_date = models.CharField(max_length=50)
    old_appt_date = models.CharField(max_length=50, null=True)
    comments = models.CharField(max_length=500)
    student_approved = models.BooleanField(default=True)
    tutor_approved = models.BooleanField(default=False)
    def __str__(self):
        return str(self.student) + " " + self.course_number
