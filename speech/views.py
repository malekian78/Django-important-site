from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Speech

# Create your views here.
def speech_list(request):
    speechList= Paginator(Speech.objects.all(),2)
    # page_number = request.GET.get('page')
    # page_number = 1
    # page_obj = paginator.get_page(page_number)
    # context={"speech_list_object":page_obj}
    
    try:
        page_number = request.GET.get('page')
        speechList = speechList.get_page(page_number)
    except PageNotAnInteger:
        speechList = speechList.get_page(1)
    except EmptyPage:
        speechList = speechList.get_page(1)
        
    context={"speechList": speechList}
        
    return render(request, 'speechList.html', context)


def speech_detail(request, speechSlug):
    theSpeech = get_object_or_404(Speech, slug = speechSlug)
    print(theSpeech)
    return render(request, 'seeechDetail.html', {'theSpeech': theSpeech})