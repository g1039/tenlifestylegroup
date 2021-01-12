# Generated by Django 3.1.5 on 2021-01-12 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('remaining_count', models.CharField(blank=True, max_length=5, null=True)),
                ('expiration_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Inventory',
            },
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('surname', models.CharField(blank=True, max_length=50, null=True)),
                ('booking_count', models.CharField(blank=True, max_length=5, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Members',
            },
        ),
    ]
