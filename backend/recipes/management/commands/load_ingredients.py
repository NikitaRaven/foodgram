import os
import csv

from django.core.management.base import BaseCommand
from django.conf import settings

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load ingredients from ingredients.csv into the database'

    def handle(self, *args, **kwargs):
        data_file_path = os.path.join(settings.BASE_DIR, 'ingredients.csv')
        ingredients_to_create = []
        existing_ingredients = set()
        for ingredient in Ingredient.objects.all():
            existing_ingredients.add(
                (ingredient.name, ingredient.measurement_unit)
            )

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
                ingredient_name = name.strip()
                ingredient_measurement_unit = measurement_unit.strip()
                ingredient_data = (
                    ingredient_name, ingredient_measurement_unit
                )

                if ingredient_data not in existing_ingredients:
                    ingredients_to_create.append(Ingredient(
                        name=ingredient_name,
                        measurement_unit=ingredient_measurement_unit
                    ))
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Will add ingredient: {ingredient_name}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Ingredient already exists: {ingredient_name}'
                        )
                    )

        if ingredients_to_create:
            Ingredient.objects.bulk_create(ingredients_to_create)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Added {len(ingredients_to_create)} ingredients.'
                )
            )
        else:
            self.stdout.write(self.style.WARNING('No new ingredients to add.'))
