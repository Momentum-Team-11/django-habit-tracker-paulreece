# Generated by Django 4.0.3 on 2022-03-22 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitapp', '0002_record_once_a_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
