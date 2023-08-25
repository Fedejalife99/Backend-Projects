# Generated by Django 4.2.1 on 2023-07-23 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_accommodation_number_of_califications_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accommodation',
            name='number_of_califications',
        ),
        migrations.RemoveField(
            model_name='accommodation',
            name='number_of_stars',
        ),
        migrations.CreateModel(
            name='Califications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calification', models.FloatField(default=0.0)),
                ('accommodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.accommodation')),
            ],
        ),
    ]
