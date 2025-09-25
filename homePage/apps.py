import logging
from django.apps import AppConfig
from django.db import connection, OperationalError

logger = logging.getLogger(__name__)


class HomepageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "homePage"
    
    #! ایجاد شده کد زیر را بنویسید migration توسط HomePage فقط وقتی که جدول
    # def ready(self):
    #     from django.db.utils import ProgrammingError
    #     try:
    #         from .models import HomePage
    #         # Check if the table exists
    #         if 'homePage_homepage' in connection.introspection.table_names():
    #             if not HomePage.objects.exists():
    #                 HomePage.objects.create()
    #         else:
    #             logger.warning("\n\n⛔ The 'HomePage' table does not exist. Did you forget to run migrations?\n\n")
    #     except (ProgrammingError, OperationalError) as e:
    #         logger.warning(f"\n\n ⛔Could not check for HomePage instance due to DB error: {e}\n\n")
