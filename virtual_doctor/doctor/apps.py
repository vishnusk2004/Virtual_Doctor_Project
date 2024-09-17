from django.apps import AppConfig


class DoctorConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'doctor'
