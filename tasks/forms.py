# forms.py
from django import forms
from .models import Task


class TaskSelectionForm(forms.Form):
    task = forms.ModelChoiceField(queryset=Task.objects.all(), empty_label="Select a task")
