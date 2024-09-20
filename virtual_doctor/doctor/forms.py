from django import forms
import requests
from requests import Response

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
        fields: list[str] = ['avatar', 'bio', 'phone_number', 'theme']
        widgets = {
            'bio': forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
            'phone_number': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'type':'tel',
                },
            ),
            'avatar': forms.ClearableFileInput(attrs={'class':'form-control-file'}),
        }
    # Override the __init__ method to dynamically populate the theme choices
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        # Initialize theme choices
        theme_choices: list[tuple[str,str]] = [('https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/cerulean/bootstrap.min.css', 'Cerulean')]

        try:
            # Fetch available themes from Bootswatch API
            response: Response = requests.get('https://bootswatch.com/api/5.json')
            response.raise_for_status()  # Raise an error for bad responses
            themes: list[dict[str,str]] = response.json().get('themes', [])

            # Generate the choices in the form of [(value, label)] where value is the CSS CDN link
            theme_choices = [(theme['cssCdn'], theme['name']) for theme in themes]

        except requests.RequestException:
            # Handle errors (you can log this if needed)
            print("Failed to fetch themes. Using default.")

        # Assign theme choices to the ChoiceField
        self.fields['theme'] = forms.ChoiceField(
            choices=theme_choices,  # Dynamic choices
            widget=forms.Select(attrs={'class': 'form-control'})  # Styling
        )
