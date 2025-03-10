from django.shortcuts import render
from django.db.models import Prefetch
from django.urls import reverse
from Word.models import *
from django.contrib.auth.decorators import login_required ,user_passes_test
from Authentication.utils import get_gravatar_url
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from Home.models import IPAddress
from datetime import timedelta
from Authentication.models import User
def Discussion(request):
    # دریافت 50 سوال آخر
    latest_questions = Ask.objects.all().order_by('-id')[:50]

    # پیش‌بارگذاری پاسخ‌ها (گرفتن دو پاسخ برای هر سؤال)
    questions_with_responses = latest_questions.prefetch_related(
        Prefetch(
            'response_set',
            queryset=Response.objects.all().order_by('id')[:2],  # دو پاسخ اول
            to_attr='responses'
        )
    )

    # ارسال گراواتار و کلمه مرتبط برای هر سوال
    questions_with_avatars_and_words = []
    for question in questions_with_responses:
        avatar_url = get_gravatar_url(question.user.email)
        word_link = question.ask_to  # فرض بر این است که هر سوال به یک کلمه مرتبط است
        questions_with_avatars_and_words.append({
            'question': question,
            'avatar': avatar_url,
            'word_link': word_link
        })

    return render(request, 'Word/discussion.html', {'questions': questions_with_avatars_and_words})

def admin_required(user):
    return user.is_superuser


"""

Admin Dashboard

"""
@user_passes_test(admin_required)
@login_required
def AdminDashboard(request):
    total_words = Words.objects.all().count()
    total_users = User.objects.all().count()
    context = {
        "total_words":total_words,
        "total_users":total_users,
    }
    return render(request, 'Admin/Home.html', context)


def daily_visits(request):
    today = now().date()
    # محاسبه روز اول هفته (7 روز گذشته)
    last_week = today - timedelta(days=6)

    # گرفتن تمامی روزهای هفته حتی با صفر بازدید
    visits = (
        IPAddress.objects
        .filter(last_seen__date__gte=last_week)  # فقط بازدیدهای 7 روز اخیر
        .annotate(day=TruncDate('last_seen'))  # گروه‌بندی بر اساس روز
        .values('day')
        .annotate(count=Count('id'))  # شمارش بازدیدهای هر روز
        .order_by('day')
    )

    # لیست روزهای هفته (حتی روزهایی که بازدید نداشتند)
    labels = [(last_week + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

    # جمع‌آوری داده‌ها و قرار دادن صفر برای روزهایی که بازدید نداشتند
    data = []
    for label in labels:
        count = next((v['count'] for v in visits if v['day'].strftime('%Y-%m-%d') == label), 0)
        data.append(count)

    return JsonResponse({"labels": labels, "data": data})

def visit_chart_view(request):
    return render(request, "visits_chart.html")  # صفحه‌ای که نمودار داره