from django.shortcuts import render , get_object_or_404 , redirect
from Word.models import Words , Suggestion , Ask , Response
from django.contrib import messages

# Create your views here.
def word_detail(request, word_slug):
    word = get_object_or_404(Words, slug=word_slug)
    suggestions = Suggestion.objects.filter(suggested_to=word, status='p')  # پیشنهادات تایید شده
    questions = Ask.objects.filter(ask_to=word)
    return render(request, 'Word/word_detail.html', {'word': word,'suggestions': suggestions, 'questions': questions})
def add_suggestion(request, word_slug):
    if request.method == "POST":
        word = get_object_or_404(Words, slug=word_slug)
        text = request.POST.get('suggestion_text')
        user = request.user

        if text:
            # ایجاد پیشنهاد جدید
            Suggestion.objects.create(
                suggested_to=word,
                user=user,
                text=text,
                status='d'  # وضعیت پیشنهادی پیش‌فرض 'د'
            )
        messages.success(request, 'پیشنهاد شما ثبت شد. پس از تایید مدیر منتشر خواهد شد.')
        return redirect('Word:word_detail', word_slug=word.slug)  # بازگشت به صفحه جزئیات کلمه
def add_question(request, word_slug):
    if request.method == "POST":
        word = get_object_or_404(Words, slug=word_slug)
        text = request.POST.get('question_text')
        user = request.user

        if text:
            # ایجاد سوال جدید
            Ask.objects.create(
                ask_to=word,
                user=user,
                question=text
            )
        return redirect('Word:word_detail', word_slug=word.slug) 
def add_response(request, question_id):
    if request.method == "POST":
        question = get_object_or_404(Ask, id=question_id)
        response_text = request.POST.get('response_text')
        user = request.user

        if response_text:
            # ذخیره پاسخ جدید
            response = Response.objects.create(
                response_to=question,
                user=user,
                response=response_text
            )
            # ارسال پیام موفقیت
            messages.success(request, 'پاسخ شما با موفقیت ارسال شد.')
        else:
            # در صورتی که متنی وارد نشده باشد
            messages.error(request, 'لطفاً یک پاسخ وارد کنید.')

        return redirect('Word:word_detail', word_slug=question.ask_to.slug)
    
import requests
from django.http import JsonResponse
from urllib.parse import quote  # استفاده از urllib.parse.quote

def get_suggestion(request, word):
    encoded_query = quote(word)  # encode کردن کلمه
    api_url = f"https://engine2.vajehyab.com/suggestion?q={encoded_query}"

    try:
        response = requests.get(api_url)
        data = response.json()
        return JsonResponse(data)  # بازگرداندن پاسخ API به‌صورت JSON
    except requests.RequestException:
        return JsonResponse({"error": "خطا در ارتباط با واژه‌یاب"}, status=500)
