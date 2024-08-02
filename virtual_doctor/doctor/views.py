<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Disease, Symptom, EmergencyContact, Appointment, HealthTip, SymptomTracker, UserProfile
from .forms import SymptomForm, EmergencyContactForm, AppointmentForm, SymptomTrackerForm
from .forms import ProfileForm
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a home or dashboard page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to a home or dashboard page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def predict_disease(request):
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            symptoms = form.cleaned_data.get('symptoms')
            symptom_list = symptoms.split(',')
            diseases = Disease.objects.all()
            predicted_diseases = []
            for disease in diseases:
                for symptom in symptom_list:
                    if symptom.strip().lower() in disease.symptoms.lower():
                        predicted_diseases.append(disease)
                        break
            return render(request, 'disease_results.html', {'diseases': predicted_diseases})
    else:
        form = SymptomForm()
    return render(request, 'predict_disease.html', {'form': form})


@login_required
def disease_detail(request, id):
    disease = get_object_or_404(Disease, id=id)
    return render(request, 'disease_detail.html', {'disease': disease})

@login_required
def manage_contacts(request):
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('manage_contacts')
    else:
        form = EmergencyContactForm()
    contacts = EmergencyContact.objects.filter(user=request.user)
    return render(request, 'manage_contacts.html', {'form': form, 'contacts': contacts})

@login_required
def schedule_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            return redirect('schedule_appointment')
    else:
        form = AppointmentForm()
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'schedule_appointment.html', {'form': form, 'appointments': appointments})

@login_required
def view_health_tips(request):
    health_tips = HealthTip.objects.all()
    return render(request, 'health_tips.html', {'health_tips': health_tips})

@login_required
def track_symptoms(request):
    if request.method == 'POST':
        form = SymptomTrackerForm(request.POST)
        if form.is_valid():
            tracker = form.save(commit=False)
            tracker.user = request.user
            tracker.save()
            return redirect('track_symptoms')
    else:
        form = SymptomTrackerForm()
    symptoms = SymptomTracker.objects.filter(user=request.user)
    return render(request, 'track_symptoms.html', {'form': form, 'symptoms': symptoms})


@login_required
def profile(request):
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=user)
        profile.save()
    return render(request, 'profile.html', {'profile': profile})

class UserProfileView(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username
    

def user_logout(request):
    logout(request)
=======
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Disease, Symptom, EmergencyContact, Appointment, HealthTip, SymptomTracker, UserProfile
from .forms import SymptomForm, EmergencyContactForm, AppointmentForm, SymptomTrackerForm
from .forms import ProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a home or dashboard page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to a home or dashboard page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def predict_disease(request):
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            symptoms = form.cleaned_data.get('symptoms')
            symptom_list = symptoms.split(',')
            diseases = Disease.objects.all()
            predicted_diseases = []
            for disease in diseases:
                for symptom in symptom_list:
                    if symptom.strip().lower() in disease.symptoms.lower():
                        predicted_diseases.append(disease)
                        break
            return render(request, 'disease_results.html', {'diseases': predicted_diseases})
    else:
        form = SymptomForm()
    return render(request, 'predict_disease.html', {'form': form})


@login_required
def disease_detail(request, id):
    disease = get_object_or_404(Disease, id=id)
    return render(request, 'disease_detail.html', {'disease': disease})

# @login_required
# def manage_contacts(request):
#     if request.method == 'POST':
#         form = EmergencyContactForm(request.POST)
#         if form.is_valid():
#             contact = form.save(commit=False)
#             contact.user = request.user
#             contact.save()
#             return redirect('manage_contacts')
#     else:
#         form = EmergencyContactForm()
#     contacts = EmergencyContact.objects.filter(user=request.user)
#     return render(request, 'manage_contacts.html', {'form': form, 'contacts': contacts})

@login_required
def manage_contacts(request):
    if request.method == 'POST':
        if 'add_contact' in request.POST:
            # Handle adding an emergency contact
            form = EmergencyContactForm(request.POST)
            if form.is_valid():
                contact = form.save(commit=False)
                contact.user = request.user
                contact.save()
                return redirect('manage_contacts')
        elif 'delete_contact' in request.POST:
            # Handle deleting an emergency contact
            contact_id = request.POST.get('contact_id')
            contact = get_object_or_404(EmergencyContact, id=contact_id, user=request.user)
            contact.delete()
            return redirect('manage_contacts')
    else:
        form = EmergencyContactForm()
    
    contacts = EmergencyContact.objects.filter(user=request.user)
    return render(request, 'manage_contacts.html', {'form': form, 'contacts': contacts})

# @login_required
# def schedule_appointment(request):
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             appointment = form.save(commit=False)
#             appointment.user = request.user
#             appointment.save()
#             return redirect('schedule_appointment')
#     else:
#         form = AppointmentForm()
#     appointments = Appointment.objects.filter(user=request.user)
#     return render(request, 'schedule_appointment.html', {'form': form, 'appointments': appointments})

@login_required
def schedule_appointment(request):
    if request.method == 'POST':
        if 'schedule' in request.POST:
            # Handle appointment scheduling
            form = AppointmentForm(request.POST)
            if form.is_valid():
                appointment = form.save(commit=False)
                appointment.user = request.user
                appointment.save()
                return redirect('schedule_appointment')
        elif 'delete' in request.POST:
            # Handle appointment deletion
            appointment_id = request.POST.get('appointment_id')
            appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
            appointment.delete()
            return redirect('schedule_appointment')
    else:
        form = AppointmentForm()
    
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'schedule_appointment.html', {'form': form, 'appointments': appointments})

@login_required
def view_health_tips(request):
    health_tips = HealthTip.objects.all()
    return render(request, 'health_tips.html', {'health_tips': health_tips})

@login_required
def track_symptoms(request):
    if request.method == 'POST':
        form = SymptomTrackerForm(request.POST)
        if form.is_valid():
            tracker = form.save(commit=False)
            tracker.user = request.user
            tracker.save()
            return redirect('track_symptoms')
    else:
        form = SymptomTrackerForm()
    symptoms = SymptomTracker.objects.filter(user=request.user)
    return render(request, 'track_symptoms.html', {'form': form, 'symptoms': symptoms})


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page or another appropriate page
    else:
        form = ProfileForm(instance=user_profile)
    
    return render(request, 'profile.html', {'form': form})

def user_logout(request):
    logout(request)
>>>>>>> c5c4e22 (On branch main)
    return redirect('login')