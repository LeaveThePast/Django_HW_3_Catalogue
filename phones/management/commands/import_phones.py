import csv

from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify

from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='The CSV file to load data from')

    def handle(self, *args, **kwargs):
        file_name = kwargs['file']
        try:
            with open(file_name, 'r') as file:
                phones = list(csv.DictReader(file, delimiter=';'))
                for phone in phones:
                    release_date = datetime.strptime(phone['release_date'], '%Y-%m-%d')
                    new_phone = Phone(
                        name=phone['name'],
                        price=phone['price'],
                        image=phone['image'],
                        release_date=release_date,
                        lte_exists=bool(phone['lte_exists']),
                        slug=slugify(phone['name'])
                    )
                    try:
                        new_phone.save()
                    except ValidationError as e:
                        print(f"Error saving {new_phone}: {e}")
        except FileNotFoundError:
            raise CommandError(f"File {file_name} not found")
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))