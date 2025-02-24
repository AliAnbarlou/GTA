from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from .extra_list import Banned
# Create your models here.
import hashlib
BANNED_DOMAINS = Banned()

def validate_email_domain(value):
    domain = value.split('@')[-1]
    if domain in BANNED_DOMAINS:
        raise ValidationError(f"متاسفیم ، اما ما این دامنه را متعبر نمیدانیم ({domain}) ، لطفا از ایمیل معتبر استفاده کنید.")
    return value

class User(AbstractUser):
    email = models.EmailField(unique=True, validators=[validate_email_domain])
    def __str__(self):
         return self.username
    def get_gravatar_url(email, size=100, default="identicon"):
        email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
        return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d={default}"
    def gravatar(self, size=100):
        return self.get_gravatar_url(self.email, size)