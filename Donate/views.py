from django.shortcuts import render , redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Donation
# Create your views here.

def verify_donation(user, amount):
    """
    تابع کمکی برای تأیید دونیت.
    در حال حاضر فقط True برمی‌گردونه.
    در آینده میشه اتصال به درگاه یا بررسی اطلاعات پرداخت رو اینجا انجام داد.
    """
    return True

@login_required
def Dontate_Success(request):
    pass


@login_required
def Donate(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount and amount.isdigit():
            amount = int(amount)
            if amount < 10000:
                error = "حداقل مقدار دونیت باید ۱۰٬۰۰۰ تومان باشد."
                return render(request, 'donate.html', {'error': error})
            
            # ذخیره در سشن برای ادامه
            request.session['donation_amount'] = amount
            return redirect('Donate:donate_confirm')
        else:
            error = "لطفاً یک مقدار معتبر وارد کنید."
            return render(request, 'donate.html', {'error': error})

    return render(request, 'donate/donate.html')

@login_required
def donate_confirm(request):
    amount = request.session.get('donation_amount')
    if not amount:
        return redirect('Donate:donate')

    if request.method == 'POST':
        # فراخوانی تابع کمکی تأیید دونیت
        if verify_donation(request.user, amount):
            # ذخیره در دیتابیس
            Donation.objects.create(user=request.user, amount=amount)
            del request.session['donation_amount']
            return render(request, 'donate_success.html', {'amount': amount})
        else:
            error = "خطا در تأیید دونیت. لطفاً مجدداً تلاش کنید."
            return render(request, 'donate_confirm.html', {'amount': amount, 'error': error})

    return render(request, 'donate/donate_confirm.html', {'amount': amount})

@login_required
def My_Donations(request):
    pass