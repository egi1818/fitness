from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    subs = [
        ("all", "All round fitness"),
        ("body_building", "Body Building"),
        ("muscle_building", "Muscle Building")
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_subscribed = models.BooleanField(default=False)
    subscribed_type = models.CharField(max_length=50, choices=subs, null=True, blank=True)
    checkout_session =models.CharField(max_length=200, null=True, blank=True)
    payment_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    message = models.TextField()

    def __str__(self):
        return self.name
