from django.contrib import admin
from .models import User , Plan , Subscription

admin.site.register(User)
admin.site.register(Plan)
admin.site.register(Subscription)