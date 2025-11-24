from django.db import models
from django.contrib.auth.models import User
from utils.base_model import BaseModel
# from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as jmodels
from jdatetime import date as jdate
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


# Create your models here.
class Speech(BaseModel):
    title = models.CharField(verbose_name=("عنوان سخنرانی"), max_length=100)
    image = models.ImageField(
        verbose_name=("تصویر بنر"), upload_to="speech/", default="speech/default.jpg"
    )
    # FIXME: گذاشته شده blank=true به صورت موقت
    audio_file = models.FileField(
        verbose_name=("فایل صوتی"),
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(["mp3", "wav", "ogg", "oga", "m4a", "aac", "flac"])
        ],
    )
    audio_link = models.CharField(
        verbose_name="لینک سخنرانی", max_length=200, blank=True, null=True,
        help_text="لینک مستقیم فایل سخنرانی (اگر سخنرانی را در جای دیگری آپلود کرده‌اید)"
    )
    slug = models.SlugField(
        verbose_name="لینک دسترسی",
        help_text="لینک منحصر به فرد برای دسترسی به این سخنرانی",
        unique=True,
    )
    category = models.ManyToManyField("Category", verbose_name=("دسته بندی"))
    tag = models.ManyToManyField("Tag", verbose_name=("تگ‌ها"), blank=True)
    visit_count = models.PositiveIntegerField(
        verbose_name=("تعداد افراد بازدید کننده"), default=0
    )
    publish_time = jmodels.jDateField(verbose_name=("تاریخ مجاز نمایش"), default=jdate.today, help_text="تاریخی که میخواهید این پست به کاربران نمایش داده شود.")
    event_date_time = jmodels.jDateField(verbose_name=("تاریخ مراسم"), default=jdate.today, help_text="تاریخی که مراسم و سخنرانی در اصل در آن تاریخ برگزار شده بود")
    first_description = models.TextField(
        verbose_name=("معرفی اولیه"), max_length=500, blank=True
    )
    lyrics=models.TextField(verbose_name="زیرنویس صوت سخنرانی", blank=True,null=True)
    complete_description = models.TextField(
        verbose_name=("توضیح کامل سخنرانی"), blank=True
    )
    #TODO: الان واجب نیست .... ولی یه کلید خارجی به یوزر بزن ... بفهمیم چه کسی این پست را ایجاد کرده

    class Meta:
        verbose_name = "سخنرانی"
        verbose_name_plural = "سخنرانی‌ها"

    def __str__(self):
        return self.title
    
    def clean(self):
        super().clean()
        if self.audio_file and self.audio_link:
            raise ValidationError("فقط یکی از فایل صوتی یا لینک سخنرانی باید پر شود، نه هر دو.")


class Category(BaseModel):
    name = models.CharField(verbose_name=("نام دسته بندی"), max_length=150)
    slug = models.SlugField(
        verbose_name=("لینک دسترسی به دسته بندی"),
        unique=True,
        help_text=("از طریق این لینک کاربران می‌توانند تمامی سخنرانی های مربوط به این دسته‌بندی را ببیند"),
    )
    parent = models.ForeignKey("self", verbose_name="والد", null=True, blank=True, related_name="children", on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("دسته‌بندی")
        verbose_name_plural = ("دسته‌بندی‌ها")

    def save(self, *args, **kwargs):
        # prevent a category to be itself parent
        if self.id and self.parent and self.id == self.parent.id:
            self.parent = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
class Tag(BaseModel):
    name = models.CharField(verbose_name=("نام تگ"), max_length=150)
    slug = models.SlugField(
        verbose_name=("لینک دسترسی به تگ"),
        unique=True,
        help_text=("از طریق این لینک کاربران می‌توانند تمامی سخنرانی های مربوط به این تگ را ببیند"),
    )

    class Meta:
        verbose_name = ("تگ")
        verbose_name_plural = ("تگ‌ها")

    def __str__(self):
        return self.name

