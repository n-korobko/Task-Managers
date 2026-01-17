from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import Worker

class WorkerRegistrationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = ("username",)