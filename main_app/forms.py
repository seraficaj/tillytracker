from django import forms
from .models import Watering

class WateringForm(forms.ModelForm):
   class Meta:
      model = Watering
      fields = ['date', 'type']
      widgets = {
         'date': forms.TextInput(attrs={
            'placeholder': 'MM/DD/YYYY'
         })
      }
