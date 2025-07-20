from django.db import models


class HomePage(models.Model):
    main_image = models.ImageField(upload_to='homepage/')
    main_description = models.TextField()

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
    
