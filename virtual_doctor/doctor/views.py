import random

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404

from doctor.forms import SymptomForm, EmergencyContactForm, AppointmentForm, SymptomTrackerForm, ProfileForm
from doctor.models import Disease, EmergencyContact, Appointment, HealthTip, SymptomTracker, UserProfile


def get_selected_theme(user: User) -> str:
    """
    Returns the selected theme for a user or a default theme if the user is not authenticated
    or does not have a profile.

    Args:
        user (User): The user for whom the theme is being selected.

    Returns:
        str: The URL of the selected or default theme.
    """
    default_theme: str = 'https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/cerulean/bootstrap.min.css'

    if not user.is_authenticated:
        return default_theme

    try:
        user_profile: UserProfile = UserProfile.objects.get(user=user)
        return user_profile.theme or default_theme
    except UserProfile.DoesNotExist:
        return default_theme


def register(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
    selected_theme: str = get_selected_theme(request.user)

    if request.method == 'POST':
        form: UserCreationForm = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username: str | None = form.cleaned_data.get('username')
            raw_password: str | None = form.cleaned_data.get('password1')
            user: User | None = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form: UserCreationForm = UserCreationForm()
    return render(request, 'register.html', {'form': form,'selected_theme': selected_theme})


def user_register(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
    selected_theme: str = get_selected_theme(request.user)

    if request.method == 'POST':
        form: UserCreationForm = UserCreationForm(request.POST)
        if form.is_valid():
            user: User = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a home or dashboard page
    else:
        form: UserCreationForm = UserCreationForm()
    return render(request, 'register.html', {'form': form,'selected_theme': selected_theme})


def user_login(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
    selected_theme: str = get_selected_theme(request.user)

    if request.method == 'POST':
        form: AuthenticationForm = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user: User = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to a home or dashboard page
    else:
        form: AuthenticationForm = AuthenticationForm()
    return render(request, 'login.html', {'form': form,'selected_theme': selected_theme})


def home(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
    selected_theme: str = get_selected_theme(request.user)

    user: User = request.user
    a_profile: UserProfile | None = None
    if user.is_authenticated:
        try:
            a_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            pass  # Handle the case where UserProfile does not exist, if needed

    return render(request, 'home.html', {'a_profile': a_profile, 'selected_theme': selected_theme})


@login_required
def predict_disease(request: WSGIRequest) -> HttpResponse:
    selected_theme: str = get_selected_theme(request.user)

    if request.method == 'POST':
        form: SymptomForm = SymptomForm(request.POST)
        if form.is_valid():
            symptoms: str | None = form.cleaned_data.get('symptoms')
            symptom_list: list[str] = symptoms.split(',')
            diseases: QuerySet[Disease] = Disease.objects.all()
            predicted_diseases: list[Disease] = []
            for disease in diseases:
                for symptom in symptom_list:
                    if symptom.strip().lower() in disease.symptoms.__str__().lower():
                        predicted_diseases.append(disease)
                        break
            return render(request, 'disease_results.html', {'diseases': predicted_diseases,'selected_theme': selected_theme})
    else:
        form: SymptomForm = SymptomForm()
    return render(request, 'predict_disease.html', {'form': form, 'selected_theme': selected_theme})


@login_required
def disease_detail(request: WSGIRequest, a_id: int) -> HttpResponse:
    selected_theme: str = get_selected_theme(request.user)

    disease: Disease = get_object_or_404(Disease, id=a_id)
    return render(request, 'disease_detail.html', {'disease': disease, 'selected_theme': selected_theme})


@login_required
def manage_contacts(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
    selected_theme: str = get_selected_theme(request.user)

    form: EmergencyContactForm = EmergencyContactForm()
    if request.method == 'POST':
        if 'add_contact' in request.POST:
            # Handle adding an emergency contact
            form: EmergencyContactForm = EmergencyContactForm(request.POST)
            if form.is_valid():
                contact: EmergencyContact = form.save(commit=False)
                contact.user = request.user
                contact.save()
                return redirect('manage_contacts')
        elif 'delete_contact' in request.POST:
            # Handle deleting an emergency contact
            contact_id: str = request.POST.get('contact_id')
            contact: EmergencyContact = get_object_or_404(EmergencyContact, id=contact_id, user=request.user)
            contact.delete()
            return redirect('manage_contacts')

    contacts: QuerySet[EmergencyContact] = EmergencyContact.objects.filter(user=request.user)
    return render(request, 'manage_contacts.html', {'form': form, 'contacts': contacts, 'selected_theme': selected_theme})


@login_required
def schedule_appointment(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
    selected_theme: str = get_selected_theme(request.user)

    if request.method == 'POST':
        if 'delete_appointment' in request.POST:  # Check if the delete button was pressed
            appointment_id: str = request.POST.get('appointment_id')
            try:
                appointment: Appointment = Appointment.objects.get(id=appointment_id, user=request.user)
                appointment.delete()
            except Appointment.DoesNotExist:
                # Handle the case where the appointment doesn't exist or doesn't belong to the user
                return HttpResponse("Appointment does not exist or you're not authorized to delete it.", status=404)
            return redirect('schedule_appointment')

        else:  # Handle appointment creation
            form: AppointmentForm = AppointmentForm(request.POST)
            if form.is_valid():
                appointment: Appointment = form.save(commit=False)
                appointment.user = request.user
                appointment.save()
                return redirect('schedule_appointment')

    else:
        form: AppointmentForm = AppointmentForm()

    appointments = Appointment.objects.filter(user=request.user)  # List all appointments for the user
    return render(request, 'schedule_appointment.html', {'form': form, 'appointments': appointments, 'selected_theme': selected_theme})


@login_required
def view_health_tips(request: WSGIRequest) -> HttpResponse:
    selected_theme: str = get_selected_theme(request.user)

    health_tips: QuerySet[HealthTip] = HealthTip.objects.all()
    images: list[str] = [
        'https://www.slohealthcenter.com/wp-content/uploads/2022/04/17-Simple-And-Useful-Health-Tips-For-Children-To-Follow-Banner-910x1024-1-910x675.jpeg',
        'https://cdn.prod.website-files.com/620e4101b2ce12a1a6bff0e8/641573b87e141d1776a71d31_Healthy%20Tips_1st%20march_header-p-1600.webp',
        'https://www.bombayhospitalindore.com/resources/assets/images/services/health-tips.jpg',
        'https://indiabreaking.com/wp-content/uploads/2024/03/tips-1.jpg',
        'https://saraldiagnostics.com/blogs/1680765834.jpg',
        'https://health.ucdavis.edu/media-resources/contenthub/post/internet/good-food/2024/02/images-body/benefits-of-walnuts.jpg',
    ]
    # Prepare health tips with a randomly selected image
    tips_with_images = [(tip, random.choice(images)) for tip in health_tips]
    return render(request, 'health_tips.html', {'selected_theme': selected_theme, 'tips_with_images': tips_with_images})


@login_required
def track_symptoms(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
    selected_theme: str = get_selected_theme(request.user)

    if request.method == 'POST':
        if 'delete_symptom' in request.POST:  # Check if the delete button was pressed
            symptom_id = request.POST.get('symptom_id')
            try:
                tracker = SymptomTracker.objects.get(id=symptom_id, user=request.user)
                tracker.delete()
            except SymptomTracker.DoesNotExist:
                # Handle case where the symptom doesn't exist or doesn't belong to the user
                return HttpResponse("Symptom does not exist or you're not authorized to delete it.", status=404)
            return redirect('track_symptoms')

        else:  # Handle symptom tracking (creation)
            form: SymptomTrackerForm = SymptomTrackerForm(request.POST)
            if form.is_valid():
                tracker: SymptomTracker = form.save(commit=False)
                tracker.user = request.user
                tracker.save()
                return redirect('track_symptoms')

    else:
        form: SymptomTrackerForm = SymptomTrackerForm()

    symptoms: QuerySet[SymptomTracker] = SymptomTracker.objects.filter(user=request.user)
    return render(request, 'track_symptoms.html', {'form': form, 'symptoms': symptoms, 'selected_theme': selected_theme})


@login_required
def profile(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
    selected_theme: str = get_selected_theme(request.user)

    user: User = request.user
    a_profile: UserProfile
    a_profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=a_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the same page after saving
    else:
        form: ProfileForm = ProfileForm(instance=a_profile)

    return render(request, 'profile.html', {'profile': a_profile, 'form': form, 'selected_theme': selected_theme})


@login_required()
def user_logout(request: WSGIRequest) -> HttpResponseRedirect:
    logout(request)
    return redirect('login')
