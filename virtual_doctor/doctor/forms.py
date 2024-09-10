from django import forms
from .models import EmergencyContact, Appointment, SymptomTracker
from .models import UserProfile


class SymptomForm(forms.Form):
    symptoms: forms.CharField = forms.CharField(widget=forms.Textarea,
                                                help_text="Enter your symptoms, separated by commas")


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields: list[str] = ['name', 'phone_number', 'relation']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields: list[str] = ['date', 'doctor_name']


class SymptomTrackerForm(forms.ModelForm):
    class Meta:
        model = SymptomTracker
        fields: list[str] = ['symptom']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields: list[str] = ['avatar', 'bio', 'phone_number']
