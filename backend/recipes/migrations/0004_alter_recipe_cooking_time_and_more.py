# Generated by Django 5.1 on 2024-09-14 16:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_recipe_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Время приготовления должно быть не менее 1 минуты.'), django.core.validators.MaxValueValidator(2147483647, 'Время приготовления не может превышать 2147483647 минут.')], verbose_name='время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Количество должно быть не менее 1.'), django.core.validators.MaxValueValidator(2147483647, 'Количество не может превыфшать 2147483647.')], verbose_name='количество'),
        ),
    ]
