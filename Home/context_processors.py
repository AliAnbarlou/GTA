from Word.models import SearchHistory, UserFavorite
from django.utils import timezone
from Word.models import mostsearchedwords
from django.db.models import Count
def account_data(request):
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59)
    top_words = (
    mostsearchedwords.objects
    .filter(searched_at__range=(today_start, today_end))
    .values('word')
    .annotate(search_count=Count('word'))
    .order_by('-search_count')[:5]
    )
    if request.user.is_authenticated:
        search_history = SearchHistory.objects.filter(user=request.user).order_by('-date')[:10]
        favorite_words = UserFavorite.objects.filter(user=request.user)

    else:
        search_history = []
        favorite_words = []
    
    return {
        'search_history': search_history,
        'favorite_words': favorite_words,
        'top_words': top_words,
    }