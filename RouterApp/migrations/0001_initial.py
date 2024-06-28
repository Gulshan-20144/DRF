# Generated by Django 4.2.11 on 2024-06-27 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Distibuter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField(null=True)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
                ('pincode', models.IntegerField(null=True)),
                ('doc_number', models.IntegerField()),
            ],
        ),
    ]