from django import forms
from .models import LostItem, FoundItem

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
