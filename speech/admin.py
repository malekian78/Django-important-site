from django.contrib import admin
from .models import CulturalGroup, Speech, Category, Tag
from django.db import models
from django.forms.widgets import ClearableFileInput
from django.utils.html import format_html


class AudioFileInput(ClearableFileInput):
    def __init__(self, *args, **kwargs):
        attrs = kwargs.get("attrs", {})
        attrs.update({"accept": ".mp3,.wav,.ogg,.oga,.m4a,.aac,.flac,audio/*"})
        kwargs["attrs"] = attrs
        super().__init__(*args, **kwargs)


# Register your models here.
class SpeechAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "slug",
        "publish_time",
        "visit_count",
        "updated_at",
        "created_at",
    )
    list_display_links = (
        "id",
        "title",
        "slug",
    )
    prepopulated_fields = {"slug": ("title",)}
    formfield_overrides = {
        models.FileField: {"widget": AudioFileInput},
    }
    list_filter = ("title", "created_at", "updated_at")
    list_editable = ("publish_time",)
    readonly_fields = ("visit_count",)
    search_fields = (
        "title",
        "publish_time",
        "author",
    )
    ordering = (
        "created_at",
        "publish_time",
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "parent",
        "slug"
    )
    prepopulated_fields = {"slug": ("name",)}


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    prepopulated_fields = {"slug": ("name",)}

@admin.register(CulturalGroup)
class SpeechOptionAdmin(admin.ModelAdmin):
    list_display = ("title", "image_preview")

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:50px;" />', obj.image.url
            )
        return "-"

admin.site.register(Speech, SpeechAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
