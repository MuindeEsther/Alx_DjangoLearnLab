from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to ='profile_pictures/', blank=True, null=True
    )
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()
    
    def follow(self, user):
        """Follow another user"""
        if user != self:
            user.followers.add(self)
    
    def unfollow(self, user):
        """Unfollow a user"""
        user.followers.remove(self)
    
    def is_following(self, user):
        """Check if this user is following another user"""
        return self.following.filter(id=user.id).exists()
    
    def is_followed_by(self, user):
        # Check if this user is followed by another user
        return self.followers.filter(id=user.id).exists()
   