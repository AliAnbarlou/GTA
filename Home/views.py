from django.shortcuts import render
#from articles.models import Article
def HomePage(request):
    return render(request,"home/Home.html")

"""
def Search_View(request):
    query = request.GET.get('q', '')
    if query:
        movie_result = Poster.objects.filter(title__icontains=query) | Poster.objects.filter(persian_title__icontains=query)
        director_results = Director.objects.filter(name__icontains=query)
        star_results = Actor.objects.filter(name__icontains=query)
    else:
        movie_result = Poster.objects.none()
        director_results = Director.objects.none()
        star_results = Actor.objects.none()
    context = {
        'query': query,
        'movie_result': movie_result,
        'director_results': director_results,
        'star_results':star_results,
    }
    return render(request, 'Home/Search_Results.html', context)"""