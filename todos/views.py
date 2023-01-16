from django.http import HttpResponse
from django.shortcuts import render
from html import escape
from .models import Todo

def index(request):
    query = Todo.objects.using('restapi')
    print("count:", query.count())

    out = ""
    for todo in query:
        print(todo)
        out = f"{out}<li>{escape(str(todo))}</li>"
    return HttpResponse(f"Testing 123: <ul>{out}</ul>")
