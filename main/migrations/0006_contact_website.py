# Generated by Django 5.0.6 on 2024-07-09 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_contact_first_name_remove_contact_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='website',
            field=models.URLField(blank=True, help_text='The website of the contact.'),
        ),
    ]
