from django.db import models
from Authentication.models import User

class Words(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # مقدار دیفالت نمی‌خواهد
    word = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, editable=True)
    meaning = models.TextField()
    example = models.TextField()

    def __str__(self):
        return self.word


class Ask(models.Model):
    ask_to = models.ForeignKey(Words, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # اینجا تغییر کرد
    question = models.TextField()

    def __str__(self):
        return self.question


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # مقدار دیفالت نمی‌خواهد
    response_to = models.ForeignKey(Ask, on_delete=models.CASCADE)
    response = models.TextField()

    def __str__(self):
        return self.response
