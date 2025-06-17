from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('freelancer', 'Freelancer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    experience = models.TextField(blank=True)
    portfolio = models.URLField(blank=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

class Project(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    timeline = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Proposal(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposals')
    cover_letter = models.TextField()
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending','Pending'),('accepted','Accepted'),('rejected','Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)