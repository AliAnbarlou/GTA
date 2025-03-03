from django.shortcuts import render , redirect
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required ,user_passes_test
from django.conf import settings
from .utils import get_gravatar_url
from django.utils import timezone
from django.db.models import Prefetch
from Word.models import Ask, Response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import User , Subscription , Plan
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class DidYouLoginOrNotView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('UserHome')
        return super().dispatch(request, *args, **kwargs)
def UserProfile(request,username):
    user = get_object_or_404(User,username=username)
    ip_address = request.user.ip_address
    if ip_address not in user.hits.all():
        user.hits.add(ip_address)
    
    return render(request, 'registration/profile.html',context={
        'site_name':settings.SITE_NAME,
        'avatar': get_gravatar_url(user.email),
        'user':user,
    })
@login_required
def UserHome(request):
    if request.user.is_superuser:
        return redirect('AdminDashboard')
    else:
        return render(request, 'registration/home.html',context={
            'site_name':settings.SITE_NAME,
            'avatar': get_gravatar_url(request.user.email),
})
    from django.contrib.auth.decorators import login_required


"""
Delete Account
"""
@login_required
def delete_account(request):
    if request.method == "POST":
        password = request.POST.get("password")
        
        if not password:
            messages.error(request, "لطفاً رمز عبور خود را وارد کنید.")
            return redirect("Authentication:delete_account")

        user = request.user
        if user.check_password(password):  # بررسی صحت رمز عبور
            user.delete()
            logout(request)
            messages.success(request, "حساب کاربری شما با موفقیت حذف شد. این عمل غیرقابل بازگشت است.")
            return redirect("home")  # تغییر مسیر به صفحه اصلی یا هر جای دیگر
        else:
            messages.error(request, "رمز عبور اشتباه است. لطفاً دوباره امتحان کنید.")
            return redirect("Authentication:delete_account")

    return render(request, "registration/delete_account.html")
"""
User profile update
"""
@login_required
def update_profile(request):
    user = request.user  # کاربر فعلی

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        bio = request.POST.get("bio")

        # اعتبارسنجی ایمیل
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "ایمیل وارد شده معتبر نیست.")
            return redirect("Authentication:update_profile")

        # بررسی اینکه ایمیل تکراری نباشد (اگر تغییر کرده باشد)
        if User.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request, "این ایمیل قبلاً استفاده شده است.")
            return redirect("Authentication:update_profile")

        # ذخیره اطلاعات جدید
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.bio = bio
        user.save()

        messages.success(request, "پروفایل شما با موفقیت بروزرسانی شد.")
        return redirect("Authentication:update_profile")

    return render(request, "registration/update_profile.html", {"user": user})
@login_required
def UserAccount(request):
    con = {
        'avatar': get_gravatar_url(request.user.email),
        'site_name': settings.SITE_NAME,
    }

    # گرفتن اشتراک کاربر
    subscription = Subscription.objects.filter(user=request.user).first()

    if subscription:
        # اگر اشتراک فعال نباشه
        if not subscription.free_subscription():
            subscription.deactive_subscription()
            # گرفتن اشتراک جدید
            subscription = Subscription.objects.filter(user=request.user).first()
            is_free_subscription = subscription.free_subscription()
            con.update({'subscription': subscription, 'is_free_subscription': is_free_subscription})
        else:
            # اشتراک رایگان فعال است
            con.update({'subscription': subscription, 'is_free_subscription': True})
    else:
        # اگر اشتراکی وجود نداشته باشه
        free_plan = Plan.objects.filter(price=0).first()
        if free_plan:
            # ایجاد اشتراک جدید برای کاربر با پلن رایگان
            Subscription.objects.create(
                user=request.user,
                plan=free_plan,
                start_date=timezone.now(),
                end_date=None,  # بدون تاریخ پایان
                is_active=True
            )
            subscription = Subscription.objects.filter(user=request.user).first()
            con.update({'subscription': subscription, 'is_free_subscription': True})
        else:
            # در صورت عدم وجود پلن رایگان
            con.update({'error_message': 'No free plan available.'})

    # بازگشت به قالب با اطلاعات موجود در context
    return render(request, 'registration/account.html', context=con)
def UserWords(request):
    pass
def UserAnswers(request):#Response
    pass
def UserQuestions(request):#Asks
    pass
def Charging(request):
    pass
def UserSuggestions(request):
    pass


def QuestionDetail(request, username, question_id):
    # دریافت کاربر (اگر نام کاربری اشتباه باشد، خطای 404 می‌دهد)
    user = get_object_or_404(User, username=username)

    # دریافت سوال مورد نظر (اگر سوال متعلق به این کاربر نباشد، باز هم 404 می‌دهد)
    question = get_object_or_404(Ask, id=question_id, user=user)

    # دریافت تمام پاسخ‌های مربوط به این سوال
    responses = Response.objects.filter(response_to=question).order_by('id')

    # پردازش فرم ارسال پاسخ
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseForbidden("برای پاسخ دادن باید وارد حساب خود شوید.")

        response_text = request.POST.get("response")
        if response_text:  # بررسی که پاسخ خالی نباشد
            Response.objects.create(
                user=request.user, 
                response_to=question, 
                response=response_text
            )
            return redirect('Authentication:QuestionDetail', username=username, question_id=question_id)  # بازگشت به همان صفحه

    return render(request, 'Word/question_detail.html', {
        'question': question,
        'responses': responses
    })
