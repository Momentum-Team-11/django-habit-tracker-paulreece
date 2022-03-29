from django import forms
from .models import User, Habit, Record


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["name", "description", "goal", "unit"]


class RecordForm(forms.ModelForm):
    date = forms.DateField(input_formats=["%m/%d/%Y"])

    class Meta:
        model = Record
        fields = ["goal_number", "date"]
