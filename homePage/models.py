from django.db import models


class HomePage(models.Model):
    main_image = models.ImageField(upload_to='homepage/', null=True, blank=True)
    main_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return "Home Page Configuration"

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Page"

class MenuItem(models.Model):
    homepage = models.ForeignKey(HomePage, related_name='menu_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relative_url = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class SlideItem(models.Model):
    homepage = models.ForeignKey(HomePage, related_name='slide_items', on_delete=models.CASCADE)
    relative_url = models.CharField(verbose_name=("آدرس url"), max_length=200, null=True, blank=True)
    image = models.ImageField(
        verbose_name=("تصویر بنر"), upload_to="speech/", default="speech/default.png"
    )

    def __str__(self):
        return self.image.name or "بدون تصویر"
    
