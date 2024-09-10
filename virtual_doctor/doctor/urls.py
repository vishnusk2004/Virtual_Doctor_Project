from django.urls import path
from doctor.views import home, predict_disease, manage_contacts, schedule_appointment, view_health_tips, track_symptoms, \
    profile, user_login, user_register, user_logout, disease_detail

urlpatterns: list[path] = [
    path('', home, name='home'),
    path('predict/', predict_disease, name='predict_disease'),
    path('contacts/', manage_contacts, name='manage_contacts'),
    path('appointments/', schedule_appointment, name='schedule_appointment'),
    path('tips/', view_health_tips, name='view_health_tips'),
    path('track/', track_symptoms, name='track_symptoms'),
    path('profile/', profile, name='profile'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('login/', user_login, name='login'),
    path('disease/<int:id>/', disease_detail, name='disease_detail'),
]
