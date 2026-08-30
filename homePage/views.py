from django.shortcuts import render
from django.core.paginator import Paginator
from speech.models import CulturalGroup, Speech


def home(request):
    groups = CulturalGroup.objects.all()
    context={"culturalGroups":groups}
    return render(request, 'homePage.html', context)