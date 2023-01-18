from datetime import datetime

from django.core.management.base import BaseCommand
from todos.models import Todo


class Command(BaseCommand):
    help = "Test todo"

    def handle(self, *args, **options):
        self.stdout.write(f"Time: {datetime.now()}")

        print("GET")
        todo = Todo.objects.using("restapi").get(pk=1)
        print(todo)

        print("UPDATE")
        todo.title = f"{todo.title}!"
        todo.save(using="restapi")
        print(todo)

        print("DELETE")
        todo.delete(using="restapi")

        print("INSERT")
        todo = Todo(user_id=123, title="Testing INSERT", completed=False)
        todo.save(using="restapi")
        print(todo)

        query = Todo.objects.using("restapi")
        self.stdout.write(f"count: {query.count()}")

        for todo in query[:15]:
            self.stdout.write(str(todo))
