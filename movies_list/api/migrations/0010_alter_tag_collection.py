# Generated by Django 4.2.2 on 2024-11-13 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_tag_collection_alter_movie_collection_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.collection'),
        ),
    ]
