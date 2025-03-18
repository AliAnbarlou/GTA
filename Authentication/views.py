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
from Word.models import Words , Suggestion , Ask , Response
from .forms import WordForm

class DidYouLoginOrNotView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('UserHome')
        return super().dispatch(request, *args, **kwargs)
def UserProfile(request, username):
    user = get_object_or_404(User, username=username)
    ip_address = request.user.ip_address
    if ip_address not in user.hits.all():
        user.hits.add(ip_address)

    # گرفتن کلمات کاربر
    # گرفتن آخرین 2 کلمه
    words = Words.objects.filter(user=user).order_by('-id')[:2]

    # گرفتن آخرین 2 پیشنهاد
    suggestions = Suggestion.objects.filter(user=user).order_by('-id')[:2]

    # گرفتن آخرین 2 سوال
    questions = Ask.objects.filter(user=user).order_by('-id')[:2]
    num_words = Words.objects.filter(user=user).count()

    # گرفتن پیشنهادات کاربر
    num_suggestions = Suggestion.objects.filter(user=user).count()
    # گرفتن سوالات کاربر
    num_questions = Ask.objects.filter(user=user).count()

    # آماده کردن داده‌ها برای ارسال به قالب
    return render(request, 'registration/profile.html', context={
        'site_name': settings.SITE_NAME,
        'avatar': get_gravatar_url(user.email),
        'user': user,
        'words': words,
        'suggestions': suggestions,
        'questions': questions,
        'num_words': num_words,
        'num_suggestions': num_suggestions,
        'num_questions': num_questions
    })

@login_required
def UserHome(request):
    if request.user.is_superuser:
        return redirect('AdminDashboard')
    context = {
        'avatar': get_gravatar_url(request.user.email),
        'site_name': settings.SITE_NAME,
    }

    # دریافت اشتراک کاربر (اگر وجود داشته باشد)
    subscription, created = Subscription.objects.get_or_create(user=request.user)

    # اگر اشتراک تازه ایجاد شده باشد (یعنی هیچ اشتراکی نداشته) یا پلن آن تنظیم نشده باشد
    if created or not subscription.plan:
        free_plan = Plan.objects.filter(price=0).first()
        if free_plan:
            subscription.plan = free_plan
            subscription.start_date = timezone.now()
            subscription.end_date = None  # بدون تاریخ پایان برای پلن رایگان
            subscription.is_active = True
            subscription.save()
        else:
            context['error_message'] = 'No free plan available.'
            return render(request, 'registration/home.html', context)

    # بررسی وضعیت اشتراک
    subscription.deactive_subscription()
    is_free_subscription = subscription.free_subscription()

    # اضافه کردن اطلاعات به context
    context.update({
        'subscription': subscription,
        'is_free_subscription': is_free_subscription,
    })

    return render(request, 'registration/home.html', context)

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
            return redirect("Home:Home")  # تغییر مسیر به صفحه اصلی یا هر جای دیگر
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
            return render(request, "registration/update_profile.html", {"user": user})

        # بررسی اینکه ایمیل تکراری نباشد (اگر تغییر کرده باشد)
        if User.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request, "این ایمیل قبلاً استفاده شده است.")
            return render(request, "registration/update_profile.html", {"user": user})

        # ذخیره اطلاعات جدید
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.bio = bio
        user.save()

        messages.success(request, "پروفایل شما با موفقیت بروزرسانی شد.")
        return redirect("Authentication:UserHome")

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
"""
USER WORDS  
"""

def UserWords(request, username):
    user = get_object_or_404(User, username=username)
    words = Words.objects.filter(user=user)

    return render(request, 'registration/user_words.html', {
        'words': words,
        'site_name': settings.SITE_NAME,
        'avatar': get_gravatar_url(user.email),
        'can_add_word': request.user == user,  # فقط خود کاربر بتواند کلمه اضافه کند
    })
@login_required
def AddWord(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            word = form.save(commit=False)
            word.user = request.user  # کاربر را به کلمه اضافه می‌کنیم
            word.save()
            return redirect('Authentication:UserWords', username=request.user.username)  # به صفحه کلمات کاربر هدایت می‌شود
    else:
        form = WordForm()

    return render(request, 'registration/add_word.html', {
        'form': form,
        'site_name': settings.SITE_NAME,
        'avatar': get_gravatar_url(request.user.email),
    })


def UserSuggestions(request , username):
    user = get_object_or_404(User, username=username)
    suggestions = user.suggestion_set.all()  # بهینه‌تر از filter()
    
    context = {
        'suggestions': suggestions,
        'site_name': getattr(settings, "SITE_NAME", "MySite"),  # مقدار پیش‌فرض در صورت نبود تنظیمات
        'avatar': get_gravatar_url(user.email),
    }
    
    return render(request, 'registration/user_suggestion.html', context)
def UserQuestions(request, username):
    # گرفتن کاربر از نام کاربری
    user = get_object_or_404(User, username=username)

    # گرفتن سوالات کاربر
    questions = Ask.objects.filter(user=user)

    # برای هر سوال، پاسخ‌های آن را هم دریافت می‌کنیم
    questions_with_responses = []
    for question in questions:
        responses = Response.objects.filter(response_to=question)
        questions_with_responses.append({
            'question': question,
            'responses': responses
        })

    return render(request, 'registration/user_questions.html', {
        'questions_with_responses': questions_with_responses,
        'site_name': settings.SITE_NAME,
        'avatar': get_gravatar_url(user.email),
    })

def QuestionDetail(request, username, question_id):
    # گرفتن سوال از ID آن
    question = get_object_or_404(Ask, id=question_id)

    # گرفتن پاسخ‌ها به این سوال
    responses = Response.objects.filter(response_to=question)

    return render(request, 'registration/question_detail.html', {
        'question': question,
        'responses': responses,
        'site_name': settings.SITE_NAME,
    })

@login_required
def Charging(request):
    plans = Plan.objects.exclude(price=0)  # فقط پلن‌های غیر رایگان را نمایش بده

    if request.method == "POST":
        plan_id = request.POST.get("plan_id")
        selected_plan = Plan.objects.filter(id=plan_id).first()

        if not selected_plan:
            messages.error(request, "پلن انتخابی معتبر نیست.")
            return redirect("Authentication:Charging")

        # بررسی اینکه آیا کاربر از قبل پلن غیررایگان دارد یا نه
        user_subscription = Subscription.objects.filter(user=request.user).first()
        if user_subscription and not user_subscription.free_subscription():
            messages.warning(request, "شما از قبل یک اشتراک فعال دارید و نمی‌توانید مجدداً خرید کنید.")
            return redirect("Authentication:Charging")

        # در اینجا باید پرداخت را پردازش کنید (بسته به سیستم پرداختی که استفاده می‌کنید)
        # به عنوان مثال، فرض می‌کنیم پرداخت موفق بوده است

        # ثبت اشتراک جدید برای کاربر
        Subscription.objects.update_or_create(
            user=request.user,
            defaults={
                "plan": selected_plan,
                "start_date": timezone.now(),
                "end_date": timezone.now() + timezone.timedelta(days=30),  # ۳۰ روز اعتبار
                "is_active": True,
            }
        )

        messages.success(request, f"پلن {selected_plan.name} با موفقیت برای شما فعال شد!")
        return redirect("Authentication:UserHome")

    return render(request, "registration/charging.html", {"plans": plans})


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

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('لینک فعال سازی به ایمیل شما ارسال شد.')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('Home:Home')
    else:
        return HttpResponse('Activation link is invalid!')
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('Authentication:password_change_done')  # مسیر را مشخص کنید
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView

class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('password_reset_done')
