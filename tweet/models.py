from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField()
    photo=models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # likes=models.PositiveIntegerField(default=0)
    # dislikes=models.PositiveIntegerField(default=0)

    def total_likes(self):
        return self.reactions.filter(reaction_type='like').count()
    
    def total_dislikes(self):
        return self.reactions.filter(reaction_type='dislike').count()

    def __str__(self):
        return f"posted by: {self.user.username}"
    
class Reaction(models.Model):
    LIKE=1
    DISLIKE=-1

    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(post, related_name='reactions', on_delete=models.CASCADE)
    reaction_type = models.CharField(choices=REACTION_CHOICES)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} {self.reaction_type}d post {self.post.id}"
            
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    profilePicture = models.ImageField(upload_to='photos/')
    dateOfBirth = models.DateField()

    def __str__(self):
        return f"profile of {self.user.username}"