# Generated by Django 3.0.6 on 2020-05-18 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_subs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dinner_Platters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('type', models.CharField(max_length=30)),
                ('price', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Pasta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Salads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.CharField(max_length=20)),
            ],
        ),
    ]