# Generated by Django 5.1.3 on 2024-12-06 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0005_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='value',
            field=models.IntegerField(choices=[(1, 'like'), (-1, 'dislike')], verbose_name='оценка'),
        ),
    ]
