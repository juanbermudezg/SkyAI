# Generated by Django 5.0.7 on 2024-07-25 06:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airliner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('path2image', models.TextField(max_length=30)),
                ('id2ai', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LocationAirport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameAirport', models.TextField(max_length=100)),
                ('nameCity', models.TextField(max_length=50)),
                ('IATA_Code', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='LocationCountry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=35, unique=True)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_number', models.CharField(max_length=10)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('day', models.IntegerField()),
                ('hourSTD', models.IntegerField()),
                ('minuteSTD', models.IntegerField()),
                ('hourSTA', models.IntegerField()),
                ('minuteSTA', models.IntegerField()),
                ('airliner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sky.airliner')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('from_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flights_departing', to='sky.locationairport')),
                ('to_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flights_arriving', to='sky.locationairport')),
            ],
        ),
        migrations.AddField(
            model_name='locationairport',
            name='nameCountry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sky.locationcountry'),
        ),
    ]
