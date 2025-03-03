from django.shortcuts import render , get_object_or_404 , redirect
from Word.models import Words , Suggestion , Ask
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