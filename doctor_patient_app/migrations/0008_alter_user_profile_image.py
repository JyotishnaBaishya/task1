# Generated by Django 3.2.5 on 2021-07-17 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_patient_app', '0007_alter_user_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Profile_Image',
            field=models.ImageField(blank=True, default='uploads/default.png', null=True, upload_to='uploads/'),
        ),
    ]