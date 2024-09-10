from django.contrib import admin
from doctor.models import UserProfile, Disease, Symptom, EmergencyContact, Appointment, HealthTip, SymptomTracker

for i in [UserProfile, Disease, Symptom, EmergencyContact, Appointment, HealthTip, SymptomTracker]:
    admin.site.register(i)
