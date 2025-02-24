from django.db import models

# Create your models here.
class IPAddress(models.Model):
    ipAddr = models.GenericIPAddressField()

    class Meta:
        verbose_name = "IP Address"
        verbose_name_plural = "IP Addresses"

    def __str__(self) -> str:
        return self.ipAddr