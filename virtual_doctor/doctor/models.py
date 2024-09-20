from django.db.models import Model, OneToOneField, CASCADE, TextField, ImageField, CharField, ForeignKey, DateTimeField
from django.contrib.auth.models import User

class UserProfile(Model):
    user: OneToOneField = OneToOneField(User, on_delete=CASCADE)
    bio: TextField = TextField(blank=True, null=True)
    avatar: ImageField = ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number: CharField = CharField(max_length=15, blank=True)
    theme: CharField = CharField(max_length=200, default='https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/cerulean/bootstrap.min.css')

    def __str__(self) -> str:
        return self.user.__str__()

class Disease(Model):
    name: CharField = CharField(max_length=100)
    symptoms: TextField = TextField()
    precautions: TextField = TextField()
    treatments: TextField = TextField()

    def __str__(self) -> str:
        return self.name.__str__()

class Symptom(Model):
    name: CharField = CharField(max_length=100)

    def __str__(self) -> str:
        return self.name.__str__()

class EmergencyContact(Model):
    user: ForeignKey = ForeignKey(User, on_delete=CASCADE)
    name: CharField = CharField(max_length=100)
    phone_number: CharField = CharField(max_length=15)
    relation: CharField = CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.name} ({self.relation})"

class Appointment(Model):
    user: ForeignKey = ForeignKey(User, on_delete=CASCADE)
    date: DateTimeField = DateTimeField()
    doctor_name: CharField = CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.user.__str__()} - {self.date} with {self.doctor_name}"

class HealthTip(Model):
    title: CharField = CharField(max_length=100)
    content: TextField = TextField()
    date_posted: DateTimeField = DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title.__str__()

class SymptomTracker(Model):
    user: ForeignKey = ForeignKey(User, on_delete=CASCADE)
    symptom: ForeignKey = ForeignKey(Symptom, on_delete=CASCADE)
    date_reported: DateTimeField = DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.__str__()} - {self.symptom.name} on {self.date_reported}"
