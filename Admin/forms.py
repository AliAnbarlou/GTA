# forms.py
from django import forms
from Word.models import Words

class WordForm(forms.ModelForm):
    class Meta:
        model = Words
        fields = ['word', 'meaning', 'example', 'status']
