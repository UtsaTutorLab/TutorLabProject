from django.forms import Form, ModelForm, Textarea
from .models import Session, Tutor, ApptDate
from datetimewidget.widgets import DateTimeWidget

class SessionForm(ModelForm):
    class Meta:
        model = Session
        fields = ['student', 'whole_name', 'classID', 'duration', 'notes']
        widgets = {'notes': Textarea(attrs={'cols':200, 'rows':10})}

