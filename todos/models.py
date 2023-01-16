from django.db import models

"""
https://jsonplaceholder.typicode.com/todos

  {
    "userId": 1,
    "id": 1,
    "title": "delectus aut autem",
    "completed": false
  },
"""

class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=True)

    def __str__(self):
        return f"Todo(id={self.id} title='{self.title} completed={self.completed}')"
