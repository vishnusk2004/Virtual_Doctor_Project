from django import forms
from doctor.models import EmergencyContact, Appointment, SymptomTracker
from doctor.models import UserProfile


class SymptomForm(forms.Form):
    symptoms: forms.CharField = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your symptoms, separated by commas',
                'rows': '3'
            }
        )
    )


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
        widgets = {
            'symptom': forms.Select(attrs={'class':'custom-select'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields: list[str] = ['avatar', 'bio', 'phone_number']
        widgets = {
            'bio': forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
            'phone_number': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'type':'tel',
                },
            ),
            'avatar': forms.FileInput(attrs={'class':'form-control-file'}),
        }
