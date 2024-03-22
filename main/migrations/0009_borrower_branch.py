# Generated by Django 5.0.3 on 2024-03-22 20:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_book_published_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrower',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.library_branch'),
        ),
    ]
