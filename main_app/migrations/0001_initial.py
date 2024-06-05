# Generated by Django 5.0.6 on 2024-06-05 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yelp_id', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('rating', models.FloatField()),
            ],
        ),
    ]
