from django.db import models


class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=True)

    class Meta:
        # https://jsonplaceholder.typicode.com/todos
        managed = False
