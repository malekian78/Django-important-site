from django.db import models

class HomePage(models.Model):
    main_image = models.ImageField(upload_to='homepage/')
    main_description = models.TextField()

    def __str__(self):
        return "Home Page Configuration"

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Page"
