# Generated by Django 3.1b1 on 2020-10-06 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0018_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='collection',
            name='movies',
            field=models.ManyToManyField(blank=True, related_query_name='collection', to='movies.Movies', verbose_name='Movies in collection'),
        ),
    ]
