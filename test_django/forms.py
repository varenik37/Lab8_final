from datetime import date
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

from django import forms
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus.widgets import DatePickerInput

from test_django.models import Assignment


class AssignmentForm(forms.ModelForm):
    date_control = forms.DateField(label="Дата сдачи", help_text="Введите дату сдачи", widget=DatePickerInput())

    class Meta:
        model = Assignment
        fields = ['number', 'salary', 'date_control', 'focus']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('number', css_class='form-control-m rounded mb-3', label_class='h5'),
            Field('salary', css_class='form-control-m rounded mb-3', label_class='h5'),
            Field('focus', css_class='form-control-m rounded mb-3', label_class='h5'),
            Submit('submit', 'Отправить', css_class='btn btn-m mt-3 mb-0 p-2 rounded-pill btn-light')
        )

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['date_control'].widget.attrs['class'] = 'datepicker'

    def clean_date(self):
        date_local = self.cleaned_data['date_control']
        print(date_local)
        print(date.today().day - date_local.day)
        difference = date.today().day - date_local.day
        if difference < 3:
            raise ValidationError("Неправильная дата")

        return date_local
