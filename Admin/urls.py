from django.urls import path , re_path
from .views import *
app_name = "Admin"


urlpatterns = [
    path('', AdminDashboard, name="AdminDashboard"),
    path('confirm_words/',ConfirmWords, name="ConfirmWords"),
    path('nowords/',NoWords,name="NoWords"),
    path('words/', AllWords, name="AllWords"),
    path('users/', AllUsers, name="AllUsers"),
    path('delete-word/<int:word_id>/', DeleteWord, name="DeleteWord"),
    path('delete-user/<int:user_id>/', DeleteUser, name="DeleteUser"),
    path('edit-word/<int:word_id>/', EditWord, name="EditWord"),
    path('edit-user/<int:user_id>/', EditUser, name="EditUser"),

    path('add-word/', AddWord, name="AddWord"),
    path('allpublished-words/', AllPublishedWords, name="AllPublishedWords"),
    path('alldonate/', AllDonate, name="AllDonate"),
    path('donate/<int:donate_id>/', Donate, name="Donate"),

]