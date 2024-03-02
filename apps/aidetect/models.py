from django.db import models


class HumanHelth(models.Model):
    anomaly_message = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    calorie = models.IntegerField()
    step_count = models.IntegerField()
    active_time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}"

class FirstStep(models.Model):
    image = models.ImageField(upload_to='first_step/')
    detected_emotion = models.CharField()
