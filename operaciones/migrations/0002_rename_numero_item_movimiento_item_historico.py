# Generated by Django 4.2.2 on 2023-06-16 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operaciones', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movimiento',
            old_name='numero_item',
            new_name='item_historico',
        ),
    ]