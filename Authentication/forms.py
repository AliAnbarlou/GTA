from django import forms
from Word.models import Words

class WordForm(forms.ModelForm):
    class Meta:
        model = Words
        fields = ['word', 'meaning', 'example']  # فیلد status حذف شده تا کاربر عادی تغییر ندهد

    def save(self, commit=True):
        word = super().save(commit=False)
        word.status = 'd'  # همیشه کلمه در حالت پیش‌نویس ذخیره شود
        if commit:
            word.save()
        return word
