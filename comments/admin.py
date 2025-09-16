from django.contrib import admin
from .models import Comment
from django.contrib.contenttypes.models import ContentType
# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "content_type":
            kwargs["queryset"] = ContentType.objects.filter(model__in = ["product"])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)