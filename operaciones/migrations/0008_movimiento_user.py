# Generated by Django 4.2.2 on 2023-06-22 21:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operaciones', '0007_alter_item_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimiento',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
            preserve_default=False,
        ),
    ]