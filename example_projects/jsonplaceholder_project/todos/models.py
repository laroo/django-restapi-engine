from django.db import models


class Todo(models.Model):
    id = models.AutoField(primary_key=True)  # type: ignore
    user_id = models.IntegerField(default=0)  # type: ignore
    title = models.CharField(max_length=200)  # type: ignore
    completed = models.BooleanField(default=True)  # type: ignore

    class Meta:
        # https://jsonplaceholder.typicode.com/todos
        managed = False
