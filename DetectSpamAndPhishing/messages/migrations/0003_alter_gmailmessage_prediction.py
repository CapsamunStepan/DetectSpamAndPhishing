# Generated by Django 4.2 on 2025-02-18 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gmail_messages', '0002_alter_gmailmessage_message_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gmailmessage',
            name='prediction',
            field=models.CharField(choices=[('no_prediction', 'NoPrediction'), ('spam', 'Spam'), ('ham', 'Ham'), ('phishing', 'Phishing')], default='ham', max_length=20),
        ),
    ]
