from django.forms import ModelForm, DateInput
from ta_tutor.models import ApptDate
from datetimewidget.widgets import DateTimeWidget
from django.forms.widgets import HiddenInput
from instructor.models import Student


class ApptDateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApptDateForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
        self.fields['student'].widget = HiddenInput()
    class Meta:
        model = ApptDate
        fields = [
            'student',
            'course_number',
            'appt_date',
            'comments',
        ]
        dateTimeOptions = {
            'format': 'mm/dd/yyyy H:ii P',
            'showMeridian' : True
        }
        widgets = {
            'appt_date': DateTimeWidget(options = dateTimeOptions, attrs={'id':"appt_date"}, bootstrap_version=3),
        }
