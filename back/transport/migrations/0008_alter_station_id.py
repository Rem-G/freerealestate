# Generated by Django 3.2 on 2021-05-05 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0007_remove_station_id_station'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]