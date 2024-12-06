# Generated by Django 5.1.3 on 2024-12-06 19:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0006_alter_rate_value'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='search_string',
            field=models.TextField(default='zxc', verbose_name='строка поиска'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rate',
            name='quote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rate', to='quotes.quote'),
        ),
        migrations.AlterField(
            model_name='rate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rate', to=settings.AUTH_USER_MODEL),
        ),
    ]