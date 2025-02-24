from django.db import models

# Create your models here.
class IPAddress(models.Model):
    ipAddr = models.GenericIPAddressField()

    class Meta:
        verbose_name = "آدرس IP"
        verbose_name_plural = "آدرس های IP"

    def __str__(self) -> str:
        return self.ipAddr