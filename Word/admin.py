from django.contrib import admin

# Register your models here.
from .models import *
# In your WordAdmin class:
class WordAdmin(admin.ModelAdmin):
    list_display = ('user', 'word', 'status',)
    list_filter = ('word', 'user', 'status',)
    search_fields = ('word',)
    ordering = ('word',)
    exclude = ("user",)  # Exclude 'user' field if not needed in form
    actions = ['make_published']
    
    # Remove prepopulated_fields
    # prepopulated_fields = {"slug": ("word",)}  # Remove this line

    def make_published(self, modeladmin, request, queryset):
        queryset.update(status='p')
    make_published.short_description = "موارد انتخاب شده را منتشر کنید"

    def save_model(self, request, obj, form, change):
        if not obj.user_id:  # بررسی می‌کنیم که مقuser` تنظیم شده یا نه
            obj.user = request.user  # تنظیم نویسنده به کاربر لاگین شده
        super().save_model(request, obj, form, change)  # ذخیره‌ی امن با `super()`
class AskAdmin(admin.ModelAdmin):
    list_display = ('ask_to',)
    list_filter = ('ask_to','user',)
    search_fields = ('ask_to',)
    ordering = ('ask_to',)
    exclude = ("user",)
    def save_model(self, request, obj, form, change):
        if not obj.user_id:  # بررسی می‌کنیم که مقuser` تنظیم شده یا نه
            obj.user = request.user  # تنظیم نویسنده به کاربر لاگین شده
        super().save_model(request, obj, form, change)  # ذخیره‌ی امن با `super()`
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('user','response_to',)
    list_filter = ('response_to','user',)
    search_fields = ('response_to',)
    ordering = ('response_to',)
    exclude = ("user",)
    def save_model(self, request, obj, form, change):
        if not obj.user_id:  # بررسی می‌کنیم که مقuser` تنظیم شده یا نه
            obj.user = request.user  # تنظیم نویسنده به کاربر لاگین شده
        super().save_model(request, obj, form, change)  # ذخیره‌ی امن با `super()`

admin.site.register(Words ,WordAdmin)
admin.site.register(Ask , AskAdmin)
admin.site.register(Response , ResponseAdmin)
admin.site.register(Suggestion)
admin.site.register(mostsearchedwords)
admin.site.register(SearchHistory)
admin.site.register(UserFavorite)