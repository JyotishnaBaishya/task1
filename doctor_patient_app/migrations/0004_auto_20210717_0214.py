# Generated by Django 3.2.5 on 2021-07-17 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_patient_app', '0003_auto_20210717_0212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
    ]