# Generated by Django 4.2.2 on 2023-10-23 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_movie_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='collection',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.collection'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.collection'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='tmdb_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tag',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.movie'),
        ),
    ]
