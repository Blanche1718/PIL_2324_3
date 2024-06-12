from django import forms
from .models import User, Preference

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'age', 'profession', 'gender', 'description']

class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = ['preferred_gender', 'age_min', 'age_max', 'preferred_profession', 'description_partner']
