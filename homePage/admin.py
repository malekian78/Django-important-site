# admin.py

from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import HomePage, MenuItem, SlideItem

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
class SlideItemInline(admin.TabularInline):
    model = SlideItem
    extra = 1

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline, SlideItemInline]
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion entirely
        return False

    def has_add_permission(self, request):
        from .models import HomePage
        return not HomePage.objects.exists()

    def changelist_view(self, request, extra_context=None):
        from .models import HomePage
        obj = HomePage.objects.first()
        if obj:
            return HttpResponseRedirect(f'/admin/homePage/homepage/{obj.id}/change/')
        return super().changelist_view(request, extra_context)
