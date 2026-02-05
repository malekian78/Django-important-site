from django.db import models
from django.contrib.auth.models import User
from utils.base_model import BaseModel

# from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as jmodels
from jdatetime import date as jdate
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
import jdatetime

User = get_user_model()

class SpeechQuerySet(models.QuerySet):
    def published(self):
        return self.filter(publish_time__lte=jdatetime.date.today())
    
# Create your models here.
class Speech(BaseModel):
    title = models.CharField(verbose_name=("عنوان سخنرانی"), max_length=100)
    image = models.ImageField(
        verbose_name=("تصویر بنر"), upload_to="speech/", default="speech/default.png"
    )
    audio_file = models.FileField(
        verbose_name=("فایل صوتی"),
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(["mp3", "wav", "ogg", "oga", "m4a", "aac", "flac"])
        ],
    )
    audio_link = models.CharField(
        verbose_name="لینک سخنرانی",
        max_length=200,
        blank=True,
        null=True,
        help_text="لینک مستقیم فایل سخنرانی (اگر سخنرانی را در جای دیگری آپلود کرده‌اید)",
    )
    slug = models.SlugField(
        verbose_name="لینک دسترسی",
        help_text="لینک منحصر به فرد برای دسترسی به این سخنرانی",
        unique=True,
    )
    category = models.ManyToManyField("Category", verbose_name=("دسته بندی"), blank=True, null=True)
    tag = models.ManyToManyField("Tag", verbose_name=("تگ‌ها"), blank=True, null=True)
    visit_count = models.PositiveIntegerField(
        verbose_name=("تعداد افراد بازدید کننده"), default=0
    )
    publish_time = jmodels.jDateField(
        verbose_name=("تاریخ مجاز نمایش"),
        default=jdate.today,
        help_text="تاریخی که میخواهید این پست به کاربران نمایش داده شود.",
    )
    event_date_time = jmodels.jDateField(
        verbose_name=("تاریخ مراسم"),
        default=jdate.today,
        help_text="تاریخی که مراسم و سخنرانی در اصل در آن تاریخ برگزار شده بود",
    )
    cultural = models.ForeignKey(
        "CulturalGroup",
        verbose_name="گروه فرهنگی",
        on_delete=models.PROTECT,
        related_name="cultural",
        null=True,
        blank=True
    )
    location = models.CharField(
        verbose_name=("مکان سخنرانی"), max_length=100, blank=True, null=True
    )
    sumary = models.TextField(verbose_name="خلاصه سخنرانی", max_length=500, blank=True, null=True)
    lyrics = models.TextField(verbose_name="زیرنویس صوت سخنرانی", blank=True, null=True)
    # TODO: الان واجب نیست .... ولی یه کلید خارجی به یوزر بزن ... بفهمیم چه کسی این پست را ایجاد کرده
    
    objects = SpeechQuerySet.as_manager() # در همه‌جا published برای استفاده از

    class Meta:
        verbose_name = "سخنرانی"
        verbose_name_plural = "سخنرانی‌ها"

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        has_file = bool(self.audio_file)
        has_link = bool(self.audio_link)

        if has_file == has_link:
            # یعنی یا هر دو پر هستند یا هر دو خالی
            raise ValidationError(
                "باید دقیقاً یکی از «فایل صوتی» یا «لینک سخنرانی» را وارد کنید."
            )


class Category(BaseModel):
    name = models.CharField(verbose_name=("نام دسته بندی"), max_length=150)
    slug = models.SlugField(
        verbose_name=("لینک دسترسی به دسته بندی"),
        unique=True,
        help_text=(
            "از طریق این لینک کاربران می‌توانند تمامی سخنرانی های مربوط به این دسته‌بندی را ببیند"
        ),
    )
    parent = models.ForeignKey(
        "self",
        verbose_name="والد",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def save(self, *args, **kwargs):
        # prevent a category to be itself parent
        if self.id and self.parent and self.id == self.parent.id:
            self.parent = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(verbose_name=("نام تگ"), max_length=150, help_text=('معمولا تک کلمه‌ای هستند'))
    slug = models.SlugField(
        verbose_name=("لینک دسترسی به تگ"),
        unique=True,
        help_text=(
            "از طریق این لینک کاربران می‌توانند تمامی سخنرانی های مربوط به این تگ را ببیند"
        ),
    )

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ها"

    def __str__(self):
        return self.name


class CulturalGroup(models.Model):
    title = models.CharField("عنوان", max_length=100)
    image = models.ImageField("تصویر", upload_to="speech/cultural/")
    slug = models.SlugField(
        verbose_name=("لینک دسترسی"),
        unique=True,
        help_text=(
            "از طریق این لینک کاربران می‌توانند تمامی سخنرانی های مربوط به این گروه فرهنگی را ببیند"
        ),
    )

    class Meta:
        verbose_name = "گروه فرهنگی"
        verbose_name_plural = "گروه‌های فرهنگی"

    def __str__(self):
        return self.title


# class Favorite(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
#     speech = models.ForeignKey("Speech", on_delete=models.CASCADE, related_name="favorites")
#     note = models.TextField(max_length=500, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ("user", "speech")  # هر کاربر فقط یک بار می‌تواند لایک کند

#     def __str__(self):
#         return f"{self.user} → {self.speech}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    speech = models.ForeignKey("Speech", on_delete=models.CASCADE, related_name="favorites")

    is_liked = models.BooleanField(default=False)
    note = models.TextField(max_length=500, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "speech")

    def __str__(self):
        return f"{self.user} → {self.speech}"

class SpeechComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    speech = models.ForeignKey("Speech", on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)