from django.db import models

# Create your models here.
# models.py

from django.db import models
from django.contrib.auth.models import User

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.token

# models.py


class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ]

    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def accept(self):
        self.status = 'accepted'
        self.save()
        # Create a Friendship relationship
        Friendship.objects.create(user=self.sender, friend=self.receiver)
        Friendship.objects.create(user=self.receiver, friend=self.sender)

    def reject(self):
        self.status = 'rejected'
        self.save()

    class Meta:
        unique_together = ('sender', 'receiver')

class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friends_with', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'friend')


        