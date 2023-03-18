import csv
import os

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'load data from csv'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Название файла')

    def handle(self, *args, **options):
        FILENAME = options['name']
        path = os.path.join('../data', FILENAME)
        with open(path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file,
                                        fieldnames=['name',
                                                    'measurement_unit'],
                                        delimiter=',')
            for row in csv_reader:
                name = row['name']
                measurement_unit = row['measurement_unit']
                ingredient = Ingredient(name=name,
                                        measurement_unit=measurement_unit)
                ingredient.save()
        self.stdout.write('Таблица с ингредиентами заполнена.')
