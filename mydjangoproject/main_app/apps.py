from django.apps import AppConfig


class MainAppConfig(AppConfig):
    verbose_name = 'Посты'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'
