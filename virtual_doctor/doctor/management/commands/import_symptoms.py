# management/commands/import_symptoms.py

import csv
from django.core.management.base import BaseCommand
from doctor.models import Symptom

class Command(BaseCommand):
    help = 'Import symptoms from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                symptom_name = row['name']
                symptom, created = Symptom.objects.get_or_create(name=symptom_name)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully added symptom: {symptom_name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Symptom already exists: {symptom_name}'))

        self.stdout.write(self.style.SUCCESS('Import process completed'))
