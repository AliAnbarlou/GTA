from django.shortcuts import render
from django.db.models import Prefetch
from django.urls import reverse
from Word.models import Ask, Response
from django.contrib.auth.decorators import login_required ,user_passes_test

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

    return render(request, 'Word/discussion.html', {'questions': questions_with_responses})
def admin_required(user):
    return user.is_superuser

@user_passes_test(admin_required)
@login_required
def AdminDashboard(request):
    return render(request, 'Admin/Home.html', {})