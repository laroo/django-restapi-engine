from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from todos.models import Todo


class Command(BaseCommand):
    help = 'Test todo'

    def handle(self, *args, **options):
        self.stdout.write(f"Time: {datetime.now()}")

        Todo.objects.using('restapi').get(pk=1)

        # todo = Todo(
        #     user_id=123,
        #     title="Testing INSERT",
        #     completed=False
        # )
        # todo.save(using="restapi")

        # query = Todo.objects.using('restapi')
        # self.stdout.write(f"count: {query.count()}")
        #
        # for todo in query:
        #     self.stdout.write(str(todo))
