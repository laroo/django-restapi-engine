from html import escape

from django.http import HttpResponse

from .models import Todo


def index(request):
    query = Todo.objects.using("restapi")

    out = ""
    for todo in query:
        out = (
            f'{out}<li><input type="checkbox" {"checked=checked" if todo.completed else ""} disabled="disabled" />'
            f"{escape(todo.title)} {todo.completed}</li>"
        )
    return HttpResponse(f"Todos: {query.count()}<ul>{out}</ul>")
