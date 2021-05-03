# Generated by Django 3.2 on 2021-04-27 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station', models.CharField(max_length=500, null=True)),
                ('network', models.CharField(max_length=500, null=True)),
                ('station_type', models.CharField(max_length=500, null=True)),
            ],
            options={
                'db_table': 'Station',
            },
        ),
    ]