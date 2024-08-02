<<<<<<< HEAD
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict_disease, name='predict_disease'),
    path('contacts/', views.manage_contacts, name='manage_contacts'),
    path('appointments/', views.schedule_appointment, name='schedule_appointment'),
    path('tips/', views.view_health_tips, name='view_health_tips'),
    path('track/', views.track_symptoms, name='track_symptoms'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('disease/<int:id>/', views.disease_detail, name='disease_detail'),
]
=======
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict_disease, name='predict_disease'),
    path('contacts/', views.manage_contacts, name='manage_contacts'),
    path('appointments/', views.schedule_appointment, name='schedule_appointment'),
    path('tips/', views.view_health_tips, name='view_health_tips'),
    path('track/', views.track_symptoms, name='track_symptoms'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('disease/<int:id>/', views.disease_detail, name='disease_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> c5c4e22 (On branch main)
