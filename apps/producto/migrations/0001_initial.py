# Generated by Django 4.2.1 on 2023-05-26 01:43

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('precio', models.FloatField()),
                ('stock', models.IntegerField(validators=[django.core.validators.MinValueValidator(0, message='El stock debe ser mayor a 0.'), django.core.validators.MaxValueValidator(100000, message='El stock debe ser menor a 100,000.')])),
            ],
            options={
                'ordering': ('nombre',),
            },
        ),
    ]
