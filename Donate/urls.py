from django.urls import path
from .views import *

app_name = 'Donate'

urlpatterns = [
    path('', Donate, name='donate'),
    path('donate_confirm/', donate_confirm, name='donate_confirm'),
    path('my-donations/', My_Donations, name='my_donations'),
]
