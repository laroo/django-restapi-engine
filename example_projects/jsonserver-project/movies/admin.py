from django.contrib import admin

from .models import Movie


class RestApiModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "genre", "rating", "is_most_watched")
    readonly_fields = ("created_at",)
    actions = None  # Disable bulk actions as filtering is not implemented in RestAPI handler
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        obj.save(using="movie_collection_api")

    def delete_model(self, request, obj):
        obj.delete(using="movie_collection_api")

    def get_queryset(self, request):
        return super().get_queryset(request).using("movie_collection_api")


admin.site.register(Movie, RestApiModelAdmin)
