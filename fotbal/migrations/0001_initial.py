# Generated by Django 2.1.5 on 2021-05-31 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tipy_fotbal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jmeno', models.CharField(max_length=20, unique=True)),
                ('tipy_skupina', models.CharField(max_length=70)),
                ('tipy_vyraz', models.CharField(max_length=70)),
            ],
            options={
                'verbose_name': 'tip fotbal',
                'verbose_name_plural': 'tipy fotbal',
            },
        ),
        migrations.CreateModel(
            name='Tymy_fotbal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skupina', models.CharField(max_length=1)),
                ('tym', models.CharField(max_length=20, unique=True)),
                ('Z', models.IntegerField()),
                ('V', models.IntegerField()),
                ('R', models.IntegerField()),
                ('P', models.IntegerField()),
                ('Gdal', models.IntegerField()),
                ('Gdostal', models.IntegerField()),
                ('skore', models.IntegerField()),
            ],
            options={
                'verbose_name': 'tým fotbal',
                'verbose_name_plural': 'týmy fotbal',
            },
        ),
        migrations.CreateModel(
            name='Zapasy_fotbal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum', models.DateField()),
                ('cas', models.TimeField()),
                ('skupina', models.CharField(max_length=1)),
                ('tyma', models.CharField(max_length=20)),
                ('tymb', models.CharField(max_length=20)),
                ('scorea', models.IntegerField()),
                ('scoreb', models.IntegerField()),
                ('vysledek', models.IntegerField()),
            ],
            options={
                'verbose_name': 'zápas fotbal',
                'verbose_name_plural': 'zápasy fotbal',
            },
        ),
    ]
