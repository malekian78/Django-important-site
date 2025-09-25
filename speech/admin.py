from django.contrib import admin
from .models import Speech


# Register your models here.
class SpeechAdmin(admin.ModelAdmin):
    list_display = ("title", "slug",)
    prepopulated_fields = {"slug": ("title",)}  # new
    
admin.site.register(Speech, SpeechAdmin)
