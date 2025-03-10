from django import forms
from Word.models import Words
from Authentication.models import User
class WordForm(forms.ModelForm):
    class Meta:
        model = Words
        fields = ['word', 'meaning', 'example']  # فیلد status حذف شده تا کاربر عادی تغییر ندهد
        exclude = ['slug']  # اضافه کردن این خط برای جلوگیری از تداخل با فیلد slug

    def save(self, commit=True):
        word = super().save(commit=False)
        word.status = 'd'  # همیشه کلمه در حالت پیش‌نویس ذخیره شود
        if commit:
            word.save()
        return word

from django.contrib.auth.forms import UserCreationForm
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2' , 'bio')
