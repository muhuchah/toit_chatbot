# Generated by Django 4.2.7 on 2023-11-26 18:24

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0004_remove_chat_vector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(default=None, null=True),
        ),
    ]
