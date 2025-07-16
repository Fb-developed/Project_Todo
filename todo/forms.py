from django import forms
from .models import Task 
from django.contrib.auth.forms import UserCreationForm 

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'is_completed']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserCreationForm.Meta.model
        fields = UserCreationForm.Meta.fields