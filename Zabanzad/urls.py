from django.contrib import admin
from django.urls import path , include
from .views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Home.urls')),
    path('word/',include('Word.urls')),
    path('translate/',include('Translate.urls')),
    path('profile/',include('Authentication.urls')),
    path('donate/',include('Donate.urls')),
    path("discussion/",view=Discussion,name="AskQuestion"),
    path('root/',include('Admin.urls')),
    path("chart/", visit_chart_view, name="visit_chart"),  # صفحه HTML نمودار
    path("api/daily-visits/", daily_visits, name="daily_visits"),  # API دریافت دا
]