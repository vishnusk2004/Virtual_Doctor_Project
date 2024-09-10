from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from doctor.forms import SymptomForm, EmergencyContactForm, AppointmentForm, SymptomTrackerForm, ProfileForm
from doctor.models import Disease, EmergencyContact, Appointment, HealthTip, SymptomTracker, UserProfile


def register(request: WSGIRequest):
    if request.method == 'POST':
        form: UserCreationForm = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form: UserCreationForm = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_register(request: WSGIRequest):
    if request.method == 'POST':
        form: UserCreationForm = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a home or dashboard page
    else:
        form: UserCreationForm = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request: WSGIRequest):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to a home or dashboard page
    else:
        form: AuthenticationForm = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def home(request: WSGIRequest):
    user = request.user
    a_profile: UserProfile | None = None
    if user.is_authenticated:
        try:
            a_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            pass  # Handle the case where UserProfile does not exist, if needed

    return render(request, 'home.html', {'a_profile': a_profile})


@login_required
def predict_disease(request: WSGIRequest):
    if request.method == 'POST':
        form: SymptomForm = SymptomForm(request.POST)
        if form.is_valid():
            symptoms = form.cleaned_data.get('symptoms')
            symptom_list: list[str] = symptoms.split(',')
            diseases = Disease.objects.all()
            predicted_diseases = []
            for disease in diseases:
                for symptom in symptom_list:
                    if symptom.strip().lower() in disease.symptoms.lower():
                        predicted_diseases.append(disease)
                        break
            return render(request, 'disease_results.html', {'diseases': predicted_diseases})
    else:
        form: SymptomForm = SymptomForm()
    return render(request, 'predict_disease.html', {'form': form})


@login_required
def disease_detail(request: WSGIRequest, a_id):
    disease: Disease = get_object_or_404(Disease, id=a_id)
    return render(request, 'disease_detail.html', {'disease': disease})


@login_required
def manage_contacts(request: WSGIRequest):
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
def schedule_appointment(request: WSGIRequest):
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
def view_health_tips(request: WSGIRequest):
    health_tips = HealthTip.objects.all()
    return render(request, 'health_tips.html', {'health_tips': health_tips})


@login_required
def track_symptoms(request: WSGIRequest):
    if request.method == 'POST':
        form: SymptomTrackerForm = SymptomTrackerForm(request.POST)
        if form.is_valid():
            tracker = form.save(commit=False)
            tracker.user = request.user
            tracker.save()
            return redirect('track_symptoms')
    else:
        form: SymptomTrackerForm = SymptomTrackerForm()
    symptoms = SymptomTracker.objects.filter(user=request.user)
    return render(request, 'track_symptoms.html', {'form': form, 'symptoms': symptoms})


@login_required
def profile(request: WSGIRequest):
    user = request.user
    a_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=a_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the same page after saving
    else:
        form = ProfileForm(instance=a_profile)

    return render(request, 'profile.html', {'profile': a_profile, 'form': form})


@login_required()
def user_logout(request: WSGIRequest):
    logout(request)
    return redirect('login')
