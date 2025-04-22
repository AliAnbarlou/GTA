from django.shortcuts import render , get_object_or_404 , redirect
from django.urls import reverse
from Word.models import(
    Words ,
    SearchHistory,
    UserFavorite,
    Suggestion,
    Ask ,
    NewWords ,
    Response
)
import requests
from django.contrib import messages
from googletrans import Translator
from .models import *
DICTIONARY_CACHE = {}

def HomePage(request):
    return render(request, "Home/Home.html")

def GrandTheftAPI(word):
    if word in DICTIONARY_CACHE:
        return DICTIONARY_CACHE[word]

    url = f"https://engine.vajehyab.com/search?q={word}&type=exact&filter=dehkhoda,moein,amid,sareh,name,en2fa,fa2en"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException:
        result = {"خطا": "خطا در دریافت اطلاعات"}
        DICTIONARY_CACHE[word] = result
        return result

    # پردازش wordbox
    dictionary_sections = data.get("wordbox", {}).get("sections", [])
    
    section_mapping = {
        "meaning": "معنی",
        "alternative": "برابر پارسی",
        "synonym": "مترادف",
        "dictionary": "لغت نامه انگلیسی"
    }


    result = {section_mapping.get(item.get("section"), item.get("section")): item.get("description", "") for item in dictionary_sections}


    dictionary_name_mapping = {
        "dehkhoda": "لغت نامه دهخدا",
        "moein": "فرهنگ فارسی معین",
        "amid": "فرهنگ فارسی عمید",
        "sareh": "واژگان فارسی سره",
        "name": "فرهنگ نام ها",
    }

    allowed_dictionaries = set(dictionary_name_mapping.keys())

    for res in data.get("results", []):
        if res.get("scope") == "exact":
            for hit in res.get("hits", []):
                dictionary_slug = hit.get("dictionarySlug", "")
                if dictionary_slug in allowed_dictionaries:
                    dictionary_name = dictionary_name_mapping[dictionary_slug]
                    result[dictionary_name] = hit.get("summary", "")

    DICTIONARY_CACHE[word] = result
    return result


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
        return redirect(f"{reverse('Home:search_words')}?q={word.word}")
  # بازگشت به صفحه جزئیات کلمه
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
        return redirect(f"{reverse('Home:search_words')}?q={word.word}")
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

        return redirect(f"{reverse('Home:search_words')}?q={question.ask_to.word}")

# views.py
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest

# views.py
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
@login_required
@require_POST
def toggle_favorite(request):
    # گزینه ۱: اگر می‌خوای json بفرستی، از این استفاده کن:
    try:
        data = json.loads(request.body)
        word_id = data.get('word_id')
    except json.JSONDecodeError:
        # fallback به form-encoded
        word_id = request.POST.get('word_id')

    if not word_id:
        return JsonResponse({'error': 'word_id missing'}, status=400)

    try:
        word = Words.objects.get(pk=word_id)
    except Words.DoesNotExist:
        return JsonResponse({'error': 'word not found'}, status=404)

    fav, created = UserFavorite.objects.get_or_create(
        user=request.user,
        favorite_word=word
    )
    if not created:
        fav.delete()
        action = 'removed'
    else:
        action = 'added'

    return JsonResponse({'action': action, 'word_id': word_id})

from django.views.decorators.csrf import ensure_csrf_cookie
@ensure_csrf_cookie
def search_words(request):
    query = request.GET.get('q', '').strip()
    context = {
        'results': [],
        'exact_match': None,
        'query': query,
    }

    if not query:
        return render(request, 'Search/search_results.html', context)
    
    # ← اینجا: اگر کاربر لاگین بود، تاریخچه را ثبت کن
    if request.user.is_authenticated:
        SearchHistory.objects.get_or_create(
            user=request.user,
            search_word=query,
        )
    # ← اینجا: اگر کاربر لاگین بود، تاریخچه را ثبت کن

    # اگر طول عبارت بیش از ۳۰ کاراکتر بود، ترجمه کن...
    if len(query) > 30:
        translator = Translator()
        languages = {
            'English': 'en',
            'German': 'de',
            'Russian': 'ru',
            'Japanese': 'ja',
            'Spanish': 'es',
            'Italian': 'it',
            'French': 'fr',
            'Dutch': 'nl'
        }
        translations = {}
        for lang_name, lang_code in languages.items():
            translations[lang_name] = translator.translate(query, dest=lang_code).text
        context['translations'] = translations

    exact_match = Words.objects.filter(word__iexact=query).first()
    results = Words.objects.filter(word__icontains=query)
    
    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(
            UserFavorite.objects.filter(user=request.user, favorite_word__in=results if not exact_match else [exact_match]).values_list('favorite_word_id', flat=True)
        )

    context['favorite_ids'] = favorite_ids
    if exact_match:
        suggestions = Suggestion.objects.filter(suggested_to=exact_match, status='p')
        questions = Ask.objects.filter(ask_to=exact_match)
        context.update({'dict': GrandTheftAPI(query)})
        context.update({
            'word': exact_match,
            'suggestions': suggestions,
            'questions': questions
        })
    else:
        if not results:
            context.update({'dict': GrandTheftAPI(query)})
            NewWords.objects.get_or_create(word=query)
            return render(request, 'Search/no_results.html', context)
        context['results'] = results
        return render(request, 'Search/search_results.html', context)

    # اضافه کردن آواتار گراواتار...
    DEFAULT_AVATAR_URL = 'https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&s=100'
    for suggestion in context.get('suggestions', []):
        suggestion.gravatar_url = (
            get_gravatar_url(suggestion.user.email)
            if suggestion.user.email else DEFAULT_AVATAR_URL
        )
    for question in context.get('questions', []):
        question.gravatar_url = (
            get_gravatar_url(question.user.email)
            if question.user.email else DEFAULT_AVATAR_URL
        )

    return render(request, 'Search/search_results.html', context)


def aboutus(request):
    about_page = get_object_or_404(StaticPages, page='a')
    return render(request, 'static/static.html', {'content': about_page.context , 'page':'درباره ما'})
def privacy(request):
    privacy_page = get_object_or_404(StaticPages, page='p')
    return render(request, 'static/static.html', {'content': privacy_page.context , 'page':'حریم خصوصی'})
def Contactus(request):
    Contactus_page = get_object_or_404(StaticPages, page='c')
    return render(request, 'static/static.html', {'content': Contactus_page.context , 'page':'ارتباط با ما'})
def faq(request):
    faq_page = get_object_or_404(StaticPages, page='f')
    return render(request, 'static/static.html', {'content': faq_page.context , 'page':'سوالات متداول'})
def mission(request):
    mission_page = get_object_or_404(StaticPages, page='m')
    return render(request, 'static/static.html', {'content':  mission_page.context , 'page':'ماموریت و چشم انداز'})




@login_required
def searchhistory(request):
    data = SearchHistory.objects.filter(user=request.user)
    return render(request, "Home/SearchHistory.html",{'data':data,})

@login_required
def favoritewords(request):
    data = UserFavorite.objects.filter(user=request.user)
    return render(request, "Home/UserFavorite.html",{'data':data,})

def socialmedia(request):
    all = SocialMedia.objects.all()
    return render(request , 'Home/socialmedias.html',{'socialmedia':all})