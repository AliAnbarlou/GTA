from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from .extra_list import Banned
from Home.models import IPAddress
from django.utils import timezone
import hashlib
BANNED_DOMAINS = Banned()

def validate_email_domain(value):
    domain = value.split('@')[-1]
    if domain in BANNED_DOMAINS:
        raise ValidationError(f"متاسفیم ، اما ما این دامنه را متعبر نمیدانیم ({domain}) ، لطفا از ایمیل معتبر استفاده کنید.")
    return value

class User(AbstractUser):
    email = models.EmailField(unique=True, validators=[validate_email_domain])
    bio = models.TextField(blank=True , max_length=100)
    hits = models.ManyToManyField(IPAddress, related_name="hits", blank=True, editable=False)
    score = models.IntegerField(default=0, editable=False)
    points_for_exemption = models.IntegerField(default=0, editable=False)
    is_banned = models.BooleanField(default=False, editable=False)

    def __str__(self):
         return self.username
    def get_gravatar_url(email, size=100, default="identicon"):
        email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
        return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d={default}"
    def gravatar(self, size=100):
        return self.get_gravatar_url(self.email, size)
    
    class Meta:
        verbose_name = "حساب"
        verbose_name_plural = "حساب ها"

class Donation(models.Model):
    donor_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    donation_date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.donor_name} - {self.amount} ریال"
class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # مبلغ اشتراک

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پلن"
        verbose_name_plural = "پلن ها"
class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription")
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    word_limit = models.IntegerField(default=5,blank=True,null=True)
    end_date = models.DateTimeField(null=True, blank=True)  # مقدار پیش‌فرض یک ماه بعد 
    is_active = models.BooleanField(default=True)
    class Meta:
        verbose_name = "اشتراک"
        verbose_name_plural = "اشتراک ها"
    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
    def free_subscription(self):
        if self.end_date is None:
            return True
        else:
            return False
        #self.end_date > timezone.now()
    def deactive_subscription(self):
        if self.end_date is None:
            pass
        else:
            if self.end_date < timezone.now():
                self.is_active = False
                self.save()
                            # دریافت پلن رایگان
                free_plan = Plan.objects.filter(price=0).first()
                if free_plan:
                    # ایجاد اشتراک جدید برای کاربر
                    Subscription.objects.create(
                        user=self.user,
                        plan=free_plan,
                        start_date=timezone.now(),
                        end_date=None,
                        is_active=True
                    )