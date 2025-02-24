from django.contrib import admin

# Register your models here.
from .models import *
class WordAdmin(admin.ModelAdmin):
    list_display = ('user','word',)
    list_filter = ('word','user',)
    search_fields = ('word',)
    ordering = ('word',)
    prepopulated_fields = {"slug": ("word",)}
    exclude = ("user",)
    def save_model(self, request, obj, form, change):
        if not obj.user_id:  # بررسی می‌کنیم که مقuser` تنظیم شده یا نه
            obj.user = request.user  # تنظیم نویسنده به کاربر لاگین شده
        super().save_model(request, obj, form, change)  # ذخیره‌ی امن با `super()`

admin.site.register(Words ,WordAdmin)
admin.site.register(Ask)
admin.site.register(Response)