# Generated by Django 3.0.6 on 2020-09-14 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freepdf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdf',
            name='slug',
            field=models.SlugField(blank=True, max_length=300, null=True),
        ),
    ]