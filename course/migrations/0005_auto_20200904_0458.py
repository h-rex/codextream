# Generated by Django 3.0.6 on 2020-09-03 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_contact_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='img',
            field=models.ImageField(upload_to='media/thumbnails'),
        ),
    ]
