from html import escape

from django.http import HttpResponse

from .models import Movie


def index(request):
    out = ""
    for movie in Movie.objects.using("movie_collection_api"):
        out = f"{out}<li>{escape(movie.title)}</li>"
    return HttpResponse(f"<ul>{out}</ul>")
