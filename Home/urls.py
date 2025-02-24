from django.urls import path
from .views import *
urlpatterns = [
    path('', view=HomePage,name="Home"),
    #path('search/', Search_View, name='Search_View'),
]