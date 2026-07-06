from django import forms
from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = [
            "title",
            "description",
            "assigned_to",
            "due_date",
            "completed"
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),

            "assigned_to": forms.Select(attrs={
                "class": "form-select"
            }),

            "due_date": forms.DateInput(attrs={
                "class": "form-control",
                "id": "due_date"
            }),

            "completed": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

    