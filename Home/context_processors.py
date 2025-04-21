from Word.models import SearchHistory, UserFavorite

def account_data(request):
    if request.user.is_authenticated:
        search_history = SearchHistory.objects.filter(user=request.user).order_by('-date')[:10]
        favorite_words = UserFavorite.objects.filter(user=request.user)
    else:
        search_history = []
        favorite_words = []
    
    return {
        'search_history': search_history,
        'favorite_words': favorite_words,
    }
