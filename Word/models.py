from django.db import models
from Authentication.models import User
from django.utils.text import slugify
import random
import string
from django.utils.text import slugify
class Words(models.Model):
    STATUS_CHOICES = [
        ('d', 'پیش نویس'),
        ('p', 'منتشر شده'),
        ('r', 'رد شده'),  # اضافه کردن وضعیت رد شده

    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    word = models.CharField(max_length=50, verbose_name="کلمه")
    slug = models.SlugField(max_length=50, unique=True, editable=False)  # Slug فقط در ایجاد ساخته شود
    meaning = models.TextField()
    example = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='d')

    def save(self, *args, **kwargs):
        # جلوگیری از تغییر وضعیت به "منتشر شده" توسط کاربران عادی
        if not self.pk:  # هنگام ایجاد کلمه جدید
            self.slug = slugify(self.word)  # تولید خودکار slug
        else:  # هنگام ویرایش
            if not self.user.is_superuser and self.status == 'p':
                self.status = 'd'  # اگر کاربر عادی سعی کرد "منتشر شده" کند، برمی‌گردانیم به "پیش نویس"
        if not self.pk:  # هنگام ایجاد کلمه جدید
            self.slug = slugify(self.word)
            # اطمینان از اینکه slug یکتا باشد
            while Words.objects.filter(slug=self.slug).exists():
                # در صورتی که slug تکراری باشد، یک پسوند تصادفی به آن اضافه می‌کنیم
                random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
                self.slug = f"{slugify(self.word)}-{random_suffix}"
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
