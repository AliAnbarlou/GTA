from django.urls import path , re_path
from .views import *
from django.contrib.auth import views as auth_views
app_name = "Authentication"


urlpatterns = [
    path("", UserHome, name="UserHome"),
    path("details/",UserAccount,name="UserAccount"),
    path("user/<str:username>/",view=UserProfile,name="UserProfile"),
    path('user/<str:username>/words/', UserWords, name='UserWords'),
    #path("user/<str:username>/answers/",view=UserAnswers,name="UserAnswers"),
    path("user/<str:username>/suggestions/", UserSuggestions, name="UserSuggestions"),  # ✅ درست
    path("charging/",view=Charging,name="Charging"),
    path("delete-account/", delete_account, name="delete_account"),
    path("update-profile/", update_profile, name="update_profile"),
    path('add/', AddWord, name="AddWord"),  # مسیر اضافه کردن کلمه
    path("user/<str:username>/questions/", view=UserQuestions, name="UserQuestions"),
    path('user/<str:username>/question/<int:question_id>/', view=QuestionDetail, name="QuestionDetail"),
    path('signup/', signup, name='signup'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),




]
urlpatterns += [
    path('login/', auth_views.LoginView.as_view(), name='login'),  # صفحه ورود
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # صفحه خروج
    
    # تغییر رمز عبور
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
urlpatterns += [
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), 
         name="password_reset"),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),


    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_form.html"), 
         name="password_reset_confirm"),

    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), 
         name="password_reset_complete"),
]