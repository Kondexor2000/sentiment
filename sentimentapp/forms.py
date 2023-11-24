from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Lekarz, Inzynier, Opinia
from django.contrib.auth import get_user_model

class LekarzRejestracjaForm(UserCreationForm):
    class Meta:
        model = Lekarz
        fields = ['username', 'email', 'password1', 'password2']

class InzynierRejestracjaForm(UserCreationForm):
    class Meta:
        model = Inzynier
        fields = ['username', 'email', 'password1', 'password2']

class OpiniaForm(forms.ModelForm):
    class Meta:
        model = Opinia
        fields = ['tresc', 'inzynier']

class LekarzLoginForm(AuthenticationForm):
    class Meta:
        model = Lekarz
        fields = ['username', 'password']

class InzynierLoginForm(AuthenticationForm):
    class Meta:
        model = Inzynier
        fields = ['username', 'password']

