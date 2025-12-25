from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Speech, Tag, Category, Favorite
from django.db.models import Q, F
import re
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


# Create your views here.
def speech_list(request):
    # allSpeech = Speech.objects.all()
    allSpeech = Speech.objects.prefetch_related("category", "tag")
    search = request.GET.get("search")
    if search:
        allSpeech = allSpeech.filter(
            Q(title__icontains=search)
            # |
            # Q(content__icontains=search)
        )

    selected_categories = request.GET.getlist("categories")
    selected_tags = request.GET.getlist("tags")

    if selected_categories:
        allSpeech = allSpeech.filter(category__id__in=selected_categories)

    if selected_tags:
        allSpeech = allSpeech.filter(tag__id__in=selected_tags)

    allSpeech = allSpeech.distinct()

    speechList = Paginator(allSpeech, 2)
    try:
        page_number = request.GET.get("page")
        speechList = speechList.get_page(page_number)
    except PageNotAnInteger:
        speechList = speechList.get_page(1)
    except EmptyPage:
        speechList = speechList.get_page(1)

    context = {
        "speechList": speechList,
        # 'categories': Category.objects.filter(parent__isnull=True)
        #     .prefetch_related('children'),
        "categories": Category.objects.filter(parent__isnull=True).prefetch_related(
            "children__children__children__children"
        ),
        "tags": Tag.objects.all(),
        "selected_categories": list(map(int, selected_categories)),
        "selected_tags": list(map(int, selected_tags)),
    }

    return render(request, "speechList.html", context)


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)

    qs = Speech.objects.filter(tag=tag).prefetch_related("tag")

    search = request.GET.get("search")
    if search:
        qs = qs.filter(Q(title__icontains=search))

    paginator = Paginator(qs, 2)
    page_number = request.GET.get("page")
    speech_list = paginator.get_page(page_number)

    context = {
        # "tag": tag,
        "speechList": speech_list,
    }

    return render(request, "speechList.html", context)


# تابع تبدیل به ثانیه
def to_seconds(t):
    m, s = t.split(":")
    return int(m) * 60 + float(s)


def speech_detail(request, speechSlug):
    theSpeech = get_object_or_404(Speech, slug=speechSlug)

    is_liked = False
    note = ''
    if request.user.is_authenticated:
        favorite = theSpeech.favorites.filter(user=request.user).first()
        if favorite:
            note = favorite.note
            is_liked = favorite.is_liked

    # برای شمارش بازدید(visit_count)
    session_key = f"visited_page_{theSpeech.id}"
    if not request.session.get(session_key):
        Speech.objects.filter(id=theSpeech.id).update(visit_count=F("visit_count") + 1)
        request.session[session_key] = True

    pattern = r"\[(\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}\.\d{3})\]\s+(.*)"
    matches = re.findall(pattern, theSpeech.lyrics)
    result = []
    for start, end, text in matches:
        result.append(
            {"start": to_seconds(start), "end": to_seconds(end), "text": text.strip()}
        )
    minute = 0
    if len(result) > 0:
        minute = int(result[-1]["end"] / 60)
    return render(
        request,
        "seeechDetail.html",
        {
            "theSpeech": theSpeech,
            "lyric": result,
            "minutes": minute,
            "is_liked": is_liked,
            "note": note
        },
    )


# @login_required # به صورت دستی میایم و ریدایرکت می کنیم با دو خط کد زیر (زیرا  درخواست فتچ از سمت جاوااسکرپیت برامون فرستاده میشه و ریدایرکت انجام نمیشه)
def toggle_favorite(request, slug):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": "/accounts/login/?next=" + request.path}, status=401)
    
    speech = get_object_or_404(Speech, slug=slug)
    fav, created = Favorite.objects.get_or_create(user=request.user, speech=speech)

    # toggle like
    fav.is_liked = not fav.is_liked
    fav.save()

    return JsonResponse({
        "liked": fav.is_liked,
        "count": speech.favorites.filter(is_liked=True).count(),
    })


# نمایش لیست سخنرانی‌های محبوب کاربر
@login_required
def my_favorites(request):
    favorites = Speech.objects.filter(favorites__user=request.user)
    return render(request, "my_favorites.html", {"favorites": favorites})

# ذخیره یادداشت خصوصی کاربر
@require_http_methods(["POST"])
def save_note(request, slug):
    if not request.user.is_authenticated:
        return redirect(f"/accounts/login/?next={request.path}")

    speech = get_object_or_404(Speech, slug=slug)
    note_text = request.POST.get("note", "").strip()

    fav, created = Favorite.objects.get_or_create(user=request.user, speech=speech)
    fav.note = note_text
    fav.save()
    
    return JsonResponse({
        "note": fav.note
    }, status=200)