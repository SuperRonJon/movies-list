# Generated by Django 4.2.2 on 2023-10-23 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='collection',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.collection'),
        ),
    ]
