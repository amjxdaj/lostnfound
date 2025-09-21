from django import forms
from .models import LostItem, FoundItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = ['title', 'description', 'location', 'date_lost', 'image', 'reward', 'phone']
        widgets = {
            "date_lost": forms.DateInput(attrs={"class": "datepicker", "placeholder": "Select a date"})

            # "date_lost": forms.DateInput(attrs={"type": "date"}),  # HTML5 calendar picker
        }


class FoundItemForm(forms.ModelForm):
    class Meta:
        model = FoundItem
        fields = ['title', 'description', 'location', 'date_found', 'image', 'phone']
        widgets = {
            "date_found": forms.DateInput(attrs={"class": "datepicker", "placeholder": "Select a date"})

            # "date_found": forms.DateInput(attrs={"type": "date"}),  # HTML5 calendar picker
        }
