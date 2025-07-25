from django.db import models
from django.contrib.auth.models import User
from utils.base_model import BaseModel
from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as jmodels

# Create your models here.
# Create your models here.
class Speech(BaseModel):
    title = models.CharField(verbose_name=_("speech title"), max_length=100)
    image = models.ImageField(upload_to='speech/', default='speech/default.jpg')
    audio_file = models.FileField(blank=True,null=True)
    # publish_time = jmodels.jDateField(verbose_name=_("publish date"))
    
    class Meta:
        verbose_name = _("speech")
        verbose_name_plural = _("speech")

    def __str__(self):
        return self.title