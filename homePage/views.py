from django.shortcuts import render
from django.core.paginator import Paginator
from speech.models import Speech


# Create your views here.
def home(request):
    paginator= Paginator(Speech.objects.all(),1)
    page_number = request.GET.get('page')
    # page_number = 1
    page_obj = paginator.get_page(page_number)
    context={"speech_list_object":page_obj}
    print("\nobject:", page_obj)
    return render(request, 'homePage.html', context)