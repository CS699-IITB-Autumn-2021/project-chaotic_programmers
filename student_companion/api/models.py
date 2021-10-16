from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class TestModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=100, blank=True, default='')
    answer = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['created_at']

class User(models.Model):
    name=models.CharField(max_length=100, blank=True, default='')
    email_id=models.EmailField()
    username=models.CharField(max_length=100, blank=True, default='')
    password=models.CharField(max_length=1000, blank=True, default='')
    user_type=models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering= ['created_at']


class FlashDeck(models.Model):
    title=models.CharField(max_length=100, blank=True, default='')
    owner_id=models.ForeignKey(User,on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering= ['title']
