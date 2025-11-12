from django.db import models
from django_jalali.db import models as jmodels


class BaseModel(models.Model):
    created_at = jmodels.jDateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)
    updated_at = jmodels.jDateTimeField(verbose_name="تاریخ به‌روزرسانی", auto_now=True)

    class Meta:
        abstract = True
        order_with_respect_to = "created_at"
