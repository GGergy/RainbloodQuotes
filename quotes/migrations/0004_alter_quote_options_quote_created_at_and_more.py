# Generated by Django 5.1.3 on 2024-12-04 18:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0003_alter_quote_author_alter_quote_full_text_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quote',
            options={'ordering': ['-created_at'], 'verbose_name': 'Цитата', 'verbose_name_plural': 'Цитаты'},
        ),
        migrations.AddField(
            model_name='quote',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]