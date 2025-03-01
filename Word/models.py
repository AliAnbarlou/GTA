from django.db import models
from Authentication.models import User

class Words(models.Model):
    STATUS_CHOICES = [
        ('d', 'پیش نویس'),
        ('p', 'منتشر شده'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # مقدار دیفالت نمی‌خواهد
    word = models.CharField(max_length=50 , verbose_name="کلمه")
    slug = models.SlugField(max_length=50, unique=True, editable=True)
    meaning = models.TextField()
    example = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='d')


    def __str__(self):
        return self.word
    class Meta:
        verbose_name = 'کلمه'
        verbose_name_plural = 'کلمه‌ها'

class Suggestion(models.Model):
    suggested_to = models.ForeignKey(Words, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # اینجا تغییر کرد
    text = models.TextField()

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
