from django.contrib import admin
from django.urls import path , include
from .views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Home.urls')),
    path('word/',include('Word.urls')),
    path('translate/',include('Translate.urls')),
    path('profile/',include('Authentication.urls')),
    path("discussion/",view=Discussion,name="AskQuestion"),
    path("root/admin/",view=AdminDashboard,name="AdminDashboard"),
]
