import os
import csv

from django.core.management.base import BaseCommand
from django.conf import settings

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load ingredients from ingredients.csv into the database'

    def handle(self, *args, **kwargs):
        data_file_path = os.path.join(settings.BASE_DIR, 'ingredients.csv')

        with open(
            data_file_path,
            newline='',
            encoding='utf-8'
        ) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) != 2:
                    self.stdout.write(
                        self.style.WARNING(f'Invalid row format: {row}')
                    )
                    continue

                name, measurement_unit = row
                ingredient, created = Ingredient.objects.get_or_create(
                    name=name.strip(),
                    measurement_unit=measurement_unit.strip()
                )

                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Added ingredient: {ingredient}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Ingredient already exists: {ingredient}'
                        )
                    )
