# Generated by Django 5.0.7 on 2024-07-18 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rouletteApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='short_description',
            new_name='shortDescription',
        ),
        migrations.RenameField(
            model_name='reciept',
            old_name='purchase_date',
            new_name='purchaseDate',
        ),
        migrations.RenameField(
            model_name='reciept',
            old_name='purchase_time',
            new_name='purchaseTime',
        ),
    ]
