from django.urls import path
from .views import *
from django.urls import path
from django.contrib.auth import views as auth_views
app_name = "Authentication"

urlpatterns = [
    path("", UserHome, name="UserHome"),
    path("details/",UserAccount,name="UserAccount"),
    path("user/<str:username>/",view=UserProfile,name="UserProfile"),
    path("user/<str:username>/words/",view=UserWords,name="UserWords"),
    path("user/<str:username>/answers/",view=UserAnswers,name="UserAnswers"),
    path("user/<str:username>/questions/",view=UserQuestions,name="UserQuestions"), #سوالات یک کاربر
    path("user/<str:username>/suggestions/",view=UserSuggestions,name="UserSuggestions"), #پیشنهادات یک کاربر
    path('user/<str:username>/question/<int:question_id>/',view=QuestionDetail,name="QuestionDetail"), #جزئیات یک سوال
    path("charging/",view=Charging,name="Charging"),
    path("delete-account/", delete_account, name="delete_account"),

]
urlpatterns += [
    path('login/', auth_views.LoginView.as_view(), name='login'),  # صفحه ورود
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # صفحه خروج
    
    # تغییر رمز عبور
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    # بازیابی رمز عبور
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
