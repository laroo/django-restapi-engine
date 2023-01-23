from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Movie(models.Model):
    id = models.AutoField(primary_key=True)  # type: ignore
    title = models.CharField(blank=False, max_length=200)  # type: ignore
    description = models.TextField(blank=False, max_length=10000)  # type: ignore
    genre = models.CharField(blank=False, max_length=200)  # type: ignore
    rating = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(10)])  # type: ignore
    country_code = models.CharField(blank=False, max_length=200)  # type: ignore
    release_date = models.DateField(
        blank=False,
    )  # type: ignore
    is_most_watched = models.BooleanField(default=False)  # type: ignore
    created_at = models.DateTimeField(default=timezone.now)  # type: ignore

    class Meta:
        db_table = "movies"  # Used to determine API endpoint
        managed = False
