from django.db import models

# Create your models here.
class IPAddress(models.Model):
    ipAddr = models.GenericIPAddressField()
    last_seen = models.DateTimeField(auto_now=True)  # ثبت آخرین زمان مشاهده

    class Meta:
        verbose_name = "آدرس IP"
        verbose_name_plural = "آدرس های IP"

    def __str__(self) -> str:
        return self.ipAddr

class ShowAds(models.Model):
    user = models.ForeignKey('Authentication.User' , on_delete=models.CASCADE)
    show = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.show}"
    
class SocialMedia(models.Model):
    STATUS_CHOICES = [
        ('i','اینستاگرام'),
        ('t','تلگرام'),
        ('f','فیسبوک'),
        ('w','واتساپ'),
    ]
    choice = models.CharField(max_length=1 , choices=STATUS_CHOICES)
    link = models.URLField()

    def __str__(self):
        return f"{self.choice} - {self.link}"
    
class StaticPages(models.Model):
    STATUS_CHOICES = [
        ('a','درباره ما'),
        ('c','ارتباط با ما'),
        ('p','حریم خصوصی'),
        ('f','سوالات متداول'),
        ('m','ماموریت و چشم انداز'),
    ]
    page = models.CharField(max_length=1 , choices=STATUS_CHOICES)
    context = models.TextField()

    def __str__(self):
        return f"{self.page} - {self.context[:20]}..."