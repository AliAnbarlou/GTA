from django.db import models
from Authentication.models import User
from django.utils.text import slugify
from unidecode import unidecode  # تبدیل حروف فارسی به لاتین
from django.utils.timezone import now

from django.utils.text import slugify
class Words(models.Model):
    STATUS_CHOICES = [
        ('d', 'پیش نویس'),
        ('p', 'منتشر شده'),
        ('r', 'رد شده'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    word = models.CharField(max_length=50, verbose_name="کلمه")
    slug = models.SlugField(max_length=50, unique=True, editable=False)  
    meaning = models.TextField()
    example = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='d')

    def save(self, *args, **kwargs):
        if not self.slug:  # فقط اگر مقدار نداشته باشد مقداردهی شود
            self.slug = slugify(unidecode(self.word))  # تبدیل فارسی به لاتین قبل از slugify
        
        # جلوگیری از تغییر وضعیت به "منتشر شده" توسط کاربران عادی
        if self.pk and not self.user.is_superuser and self.status == 'p':
            self.status = 'd'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.word
    class Meta:
        verbose_name = 'کلمه'
        verbose_name_plural = 'کلمه‌ها'

class Suggestion(models.Model):
    STATUS_CHOICES = [
        ('d', 'پیش نویس'),
        ('p', 'منتشر شده'),
        ('r', 'رد شده'),  # اضافه کردن وضعیت رد شده
    ]
    suggested_to = models.ForeignKey(Words, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # اینجا تغییر کرد
    text = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='d')

    def __str__(self):
        return self.text
    class Meta:
        verbose_name = 'پیشنهاد'
        verbose_name_plural = 'پیشنهادات '

class Ask(models.Model):
    ask_to = models.ForeignKey(Words, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # اینجا تغییر کرد
    question = models.TextField()

    def __str__(self):
        return self.question
    class Meta:
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات'

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # مقدار دیفالت نمی‌خواهد
    response_to = models.ForeignKey(Ask, on_delete=models.CASCADE)
    response = models.TextField()

    def __str__(self):
        return self.response
    class Meta:
        verbose_name = 'پاسخ'
        verbose_name_plural = 'پاسخ‌ها'
class NewWords(models.Model):
    word = models.CharField(max_length=50, verbose_name="کلمه")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word
    
class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_word = models.CharField(max_length=100)
    date = models.DateField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.search_word}"

# models.py
class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_word = models.ForeignKey(Words, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'favorite_word')

    def __str__(self):
        return f"{self.user.username} - {self.favorite_word.word}"
