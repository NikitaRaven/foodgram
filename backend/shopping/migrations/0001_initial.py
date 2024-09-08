# Generated by Django 5.1 on 2024-09-08 19:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_list', to='recipes.recipe', verbose_name='рецепт')),
            ],
            options={
                'verbose_name': 'корзина покупок',
                'verbose_name_plural': 'коризны покупок',
            },
        ),
    ]
