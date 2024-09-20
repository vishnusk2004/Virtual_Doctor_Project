import csv
from django.core.management.base import BaseCommand
from doctor.models import HealthTip  # Replace with your actual app name

class Command(BaseCommand):
    help = 'Import health tips from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the CSV file to import')

    def handle(self, *args, **kwargs):
        file_path: str = kwargs['file_path']
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    a_title = row["title"]
                    health_tip, created = HealthTip.objects.get_or_create(
                        title=a_title,
                        content=row["content"],
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added Health Tip: {a_title}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Health Tip already exists: {a_title}'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('CSV file not found.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
