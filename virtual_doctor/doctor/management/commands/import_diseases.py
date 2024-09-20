# management/commands/import_diseases.py

import csv
from django.core.management.base import BaseCommand
from doctor.models import Disease

class Command(BaseCommand):
    help = 'Import diseases from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                a_name = row['name']
                disease, created = Disease.objects.get_or_create(
                    name=a_name,
                    symptoms=row['symptoms'],
                    precautions=row['precautions'],
                    treatments=row['treatments']
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully added Disease: {a_name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Disease already exists: {a_name}'))

        self.stdout.write(self.style.SUCCESS('Successfully imported diseases'))
