# Generated by Django 3.2.5 on 2021-07-19 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_patient_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('MH', 'Mental Health'), ('HD', 'Heart Disease'), ('CV', 'Covid19'), ('IM', 'Immunisation')], max_length=2),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='posts/default.png', upload_to='post/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='summary',
            field=models.TextField(max_length=500),
        ),
    ]