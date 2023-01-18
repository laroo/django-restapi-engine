from django.contrib import admin

from .models import Todo


class RestApiModelAdmin(admin.ModelAdmin):
    using = "restapi"

    list_display = ("id", "title", "completed", "user_id")
    actions = None  # Disable bulk actions as filtering is not implemented in RestAPI handler
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)


admin.site.register(Todo, RestApiModelAdmin)
