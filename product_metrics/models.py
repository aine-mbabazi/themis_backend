from django.db import models

# Create your models here.


class ProductMetrics(models.Model):
    date = models.DateField(unique=True)  # Ensure each date is unique
    signups = models.IntegerField(default=0)  # Number of signups
    transcribed_cases = models.IntegerField(default=0)  # Number of generated case briefs
    active_users = models.IntegerField(default=0)  # Number of active users
    average_processing_time = models.FloatField(default=0.0)  # Average processing time in seconds

    def __str__(self):
        return f"{self.date}: {self.signups} signups, {self.transcribed_cases} transcribed cases, {self.active_users} active users"
