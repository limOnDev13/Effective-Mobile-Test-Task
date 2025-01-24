# Generated by Django 5.1.5 on 2025-01-23 08:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('table_number', models.IntegerField(help_text='Номер стола', validators=[django.core.validators.MinValueValidator(0)])),
                ('status', models.CharField(choices=[('pending', 'в ожидании'), ('done', 'готово'), ('paid', 'оплачено')], default='в ожидании', help_text='Статус заказа: “в ожидании”, “готово”, “оплачено”')),
                ('items', models.ManyToManyField(help_text='Список блюд в заказе', to='menu.dish')),
            ],
        ),
    ]
