from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Speech

# Create your views here.
def speech_list(request):
    posts= Paginator(Speech.objects.all(),2)
    # page_number = request.GET.get('page')
    # page_number = 1
    # page_obj = paginator.get_page(page_number)
    # context={"speech_list_object":page_obj}
    
    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)
        
    context={"posts": posts}
        
    return render(request, 'speechList.html', context)