from django import forms
from .models import Agenda
from django.db.models import Q
from django.utils.timezone import localdate


class AgendaForm(forms.ModelForm):
    def clean(self):
        if self.cleaned_data['dia'] < localdate():
            raise forms.ValidationError('Data anterior ao dia de hoje')
        if Agenda.objects.filter(Q(dia=self.cleaned_data["dia"]) & Q(medico=self.cleaned_data["medico"])).exists():
            raise forms.ValidationError('Medico já tem uma agenda para esse dia')
        return self.cleaned_data