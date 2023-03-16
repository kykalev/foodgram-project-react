import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient

MYPATH = '../data'
FILENAME = 'ingredients.csv'


class Command(BaseCommand):
    help = 'load data from csv'

    def handle(self, *args, **options):
        with open(MYPATH + '/' + FILENAME, encoding='utf-8') as csv_file:
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
        print('Таблица с ингредиентами заполнена.')
