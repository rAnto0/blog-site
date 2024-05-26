from django.apps import AppConfig


class MainAppConfig(AppConfig):
    verbose_name = 'Статьи'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'
