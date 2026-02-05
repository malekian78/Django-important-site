from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Speech, Tag, Category, Favorite
from django.db.models import Q, F
import re
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import random
import string
from datetime import timedelta
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from jdatetime import date as jdate
from jdatetime import datetime as jdatetime
from pathlib import Path

def save_default_data():
    BASE_DIR = Path("F:/WebScripting/WebScripingTutorial/eitaa/toSaveDatabase")

    def extract_index(folder_name: str) -> int:
        """
        استخراج اندیس عددی فولدر
        مثال:
        '10-1404-7-24' -> 10
        '21' -> 21
        """
        return int(folder_name.split('-')[0])
    
    def random_string(length=8):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


    txt_files = []

    folders = sorted(
        (f for f in BASE_DIR.iterdir() if f.is_dir()),
        key=lambda f: extract_index(f.name)
    )

    for folder in folders:
        # گرفتن txt داخل فولدر
        txts = list(folder.glob('*.txt'))

        if not txts:
            raise FileNotFoundError(f"No txt file found in {folder}")

        if len(txts) > 1:
            raise RuntimeError(f"Multiple txt files found in {folder}")

        txt_files.append(txts[0])


    # خروجی نهایی
    for i, txt in enumerate(txt_files):
        print(i, txt)




    def parse_txt_content(text: str):
        # MessageLink
        message_link_match = re.search(r'MessageLink:(.+)', text)
        message_link = message_link_match.group(1).strip() if message_link_match else None

        # DocumentURL
        document_url_match = re.search(r'DocumentURL:(.+)', text)
        document_url = document_url_match.group(1).strip() if document_url_match else None

        # تاریخ (فرمت yyyy-mm-dd)
        date_match = re.search(r'\b\d{4}-\d{1,2}-\d{1,2}\b', text)
        date = date_match.group(0) if date_match else None

        # متن اصلی (همه چیز قبل از MessageLink)
        if message_link_match:
            main_text = text[:message_link_match.start()].strip()
        else:
            main_text = text.strip()

        return {
            "main_text": main_text,
            "message_link": message_link,
            "date": date,
            "document_url": document_url
        }
        

    for txtF in txt_files:    
        with open(str(txtF), "r", encoding="utf-8") as f:
            content = f.read()

        result = parse_txt_content(content)
        # print("متن اصلی:\n", result["main_text"])
        # print("\nMessageLink:", result["message_link"])
        # print("Date:", result["date"])
        # print("DocumentURL:", result["document_url"])
        # print("____________________________________")
        # print("____________________________________")
        
        # تبدیل تاریخ جلالی
        # event_date = jdate.fromisoformat(result["date"]) // Invalid isoformat string: '1404-10-4'
        event_date = jdatetime.strptime(result["date"], "%Y-%m-%d").date()

        # ساخت title
        title = result["date"] or f"speech-{random_string()}"

        # ساخت slug
        slug = slugify(title, allow_unicode=True)
        if not slug:
            slug = random_string()

        # publish_time = سه ماه بعد
        publish_time = event_date + timedelta(days=90)

        speech = Speech(
            title=title,
            audio_file=None,
            audio_link=result["document_url"],
            slug=slug,
            publish_time=publish_time,
            event_date_time=event_date,
            cultural=None,
            location="مقبره علامه مجلسی(ع)",
            sumary=result["main_text"],
            lyrics=None,
        )

        # اجرای clean مدل (خیلی مهم)
        speech.full_clean()
        speech.save()



def speech_list(request):
    # allSpeech = Speech.objects.all()
    today = jdate.today()
    # allSpeech = Speech.objects.prefetch_related("category", "tag").filter(
    #     publish_time__lte=today
    # )
    allSpeech = Speech.objects.prefetch_related("category", "tag").published()

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
    matches = re.findall(pattern, theSpeech.lyrics or "")
    result = []
    has_timing = bool(matches)

    if has_timing:
        for start, end, text in matches:
            result.append({
                "start": to_seconds(start),
                "end": to_seconds(end),
                "text": text.strip()
            })
    else:
        # متن خالص – فقط یک آیتم
        if theSpeech.lyrics:
            result.append({
                "start": None,
                "end": None,
                "text": theSpeech.lyrics.strip()
            })
    
    return render(
        request,
        "seeechDetail.html",
        {
            "theSpeech": theSpeech,
            "lyric": result,
            "has_timing": has_timing,
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