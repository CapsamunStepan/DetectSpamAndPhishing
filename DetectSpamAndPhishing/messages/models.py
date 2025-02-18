from django.db import models


# Create your models here.
class GmailUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    gmail = models.TextField(unique=True)
    total_messages = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.gmail


class GmailMessage(models.Model):
    PREDICTION_CHOICES = (
        ('no_prediction', 'NoPrediction'),
        ('spam', 'Spam'),
        ('ham', 'Ham'),
        ('phishing', 'Phishing'),
    )

    message_id = models.IntegerField(primary_key=True, unique=True, auto_created=True)
    gmail_id = models.IntegerField()
    subject = models.TextField()
    body = models.TextField()
    sender = models.TextField()
    receiver = models.ForeignKey(GmailUser, on_delete=models.CASCADE)
    received_at = models.DateTimeField()
    prediction = models.CharField(max_length=20, choices=PREDICTION_CHOICES, default='no_prediction')

    class Meta:
        ordering = ['-received_at']
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return str(self.receiver) + " - " + str(self.gmail_id)

