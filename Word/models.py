from django.db import models

# Create your models here.
class Words(models.Model):
    word = models.CharField(max_length=50)
    meaning = models.TextField()
    example = models.TextField()
    def __str__(self):
        return self.word
    
class Ask(models.Model):
    question = models.TextField()
    answer = models.TextField()
    def __str__(self):
        return self.question