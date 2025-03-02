from django.contrib import admin
from .models import IPAddress

@admin.register(IPAddress)
class IPAddressAdmin(admin.ModelAdmin):
    list_display = ("ipAddr", "last_seen")  # نمایش هر دو فیلد در لیست
    ordering = ("-last_seen",)  # مرتب‌سازی بر اساس آخرین بازدید (جدیدترین‌ها بالا)
    search_fields = ("ipAddr",)  # امکان جستجو بر اساس IP
