# Generated by Django 3.2.9 on 2023-01-17 16:27

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Todo",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("user_id", models.IntegerField(default=0)),
                ("title", models.CharField(max_length=200)),
                ("completed", models.BooleanField(default=True)),
            ],
            options={
                "managed": False,
            },
        ),
    ]
