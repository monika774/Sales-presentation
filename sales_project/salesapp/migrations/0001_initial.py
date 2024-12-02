# Generated by Django 5.1.3 on 2024-12-02 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SalesData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('product', models.CharField(max_length=20)),
                ('sales', models.FloatField()),
                ('region', models.CharField(max_length=20)),
            ],
        ),
    ]
