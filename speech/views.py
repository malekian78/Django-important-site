from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Speech
from django.db.models import Q

# Create your views here.
def speech_list(request):
    allSpeech = Speech.objects.all()
    search = request.GET.get('search')
    if search:
        allSpeech = allSpeech.filter(
            Q(title__icontains=search) 
            # |
            # Q(content__icontains=search)
        )
        
        
    speechList= Paginator(allSpeech,2)
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