# Generated by Django 4.2.2 on 2023-06-22 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operaciones', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='defectos',
        ),
        migrations.AddField(
            model_name='item',
            name='defectos',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
