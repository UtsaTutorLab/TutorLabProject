from django.contrib import admin
import nested_admin
from .models import Survey, Question, Choice

class SurveyAdmin(nested_admin.NestedModelAdmin):
    list_display = ['tutor', 'date_completed']
    search_fields = ['tutor', 'comment_text']
    list_filter = ['date_completed']
    class meta:
        model=Survey
        
class QuestionAdmin(admin.ModelAdmin):
    model = Question
    extra = 0

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)


