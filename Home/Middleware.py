from django.utils.timezone import now
from .models import IPAddress

class SaveIPMiddleware:
    def __init__(self , get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        ip_address, created = IPAddress.objects.update_or_create(
            ipAddr=ip,
            defaults={"last_seen": now()}  # به‌روزرسانی زمان آخرین بازدید
        )

        request.user.ip_address = ip_address  # اتصال IP به کاربر
        response = self.get_response(request)

        return response
