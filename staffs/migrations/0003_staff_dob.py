# Generated by Django 4.2 on 2023-12-30 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffs', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
