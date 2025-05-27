# admin.py

from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import HomePage

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Prevent adding new objects if one already exists
        return not HomePage.objects.exists()

    def changelist_view(self, request, extra_context=None):
        obj = HomePage.objects.first()
        if obj:
            return HttpResponseRedirect(f'/admin/homePage/homepage/{obj.id}/change/')
        return super().changelist_view(request, extra_context)
