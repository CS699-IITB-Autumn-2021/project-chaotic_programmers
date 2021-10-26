# Generated by Django 3.2.7 on 2021-10-26 13:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_flashcarduser_revision_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flashcarduser',
            name='revision_at',
        ),
        migrations.AddField(
            model_name='flashcard',
            name='next_scheduled_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]