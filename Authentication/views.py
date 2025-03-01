from django.shortcuts import render , redirect
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .utils import get_gravatar_url
from django.utils import timezone

from .models import User , Subscription , Plan
class DidYouLoginOrNotView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('UserHome')
        return super().dispatch(request, *args, **kwargs)

@login_required
def UserHome(request):
    return render(request, 'registration/home.html',context={'site_name':settings.SITE_NAME})
@login_required
def UserAccount(request):
    # تعریف context اصلی
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
