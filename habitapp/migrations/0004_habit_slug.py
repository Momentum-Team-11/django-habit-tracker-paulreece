# Generated by Django 4.0.3 on 2022-03-23 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitapp', '0003_alter_record_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]