from django.forms import ModelForm, DateInput
from datetimewidget.widgets import DateTimeWidget, DateWidget
from .models import Term
from django.forms.widgets import HiddenInput

class AddTermForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddTermForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

    class Meta:
        model = Term
        fields = [
            'name',
            'start',
            'end',
        ]
        dateOptions = {
            'format': 'mm/dd/yyyy',
            'showMeridian' : True
        }
        widgets = {
            'start_date': DateWidget(options = dateOptions, attrs={'id':"start_date"}, bootstrap_version=3),
            'end_date': DateWidget(options = dateOptions, attrs={'id':"end_date"}, bootstrap_version=3),
        }
