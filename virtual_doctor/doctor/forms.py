from django import forms
from .models import Symptom, EmergencyContact, Appointment, SymptomTracker
from .models import UserProfile

class SymptomForm(forms.Form):
    symptoms = forms.CharField(widget=forms.Textarea, help_text="Enter your symptoms, separated by commas")

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'phone_number', 'relation']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'doctor_name']

class SymptomTrackerForm(forms.ModelForm):
    class Meta:
        model = SymptomTracker
        fields = ['symptom']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'phone_number']