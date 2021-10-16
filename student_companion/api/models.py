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
    name = models.CharField(max_length=100, blank=False, default='')
    email_id = models.EmailField()
    username = models.CharField(max_length=100, blank=False, default='')
    password = models.CharField(max_length=1000, blank=False, default='')
    user_type = models.CharField(max_length=100, blank=False, default='normal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering= ['created_at']


class FlashDeck(models.Model):
    title = models.CharField(max_length=100, blank=False, default='')
    owner_id = models.ForeignKey(User,on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering= ['title']


class UserRelation(models.Model):
    related_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Flashcard(models.Model):
    title = models.CharField(max_length=100, blank = False, default='')
    question = models.CharField(max_length=100, blank = False, default='')
    answer = models.CharField(max_length=100, blank = False, default='')
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    flash_deck_id = models.ForeignKey(FlashDeck, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class FlashcardUser(models.Model):
    flashcard_id = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    last_opened = models.DateTimeField()
    last_time_taken = models.IntegerField()
    next_scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=10, blank = False, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class ActivityMonitor(models.Model):
    date = models.DateTimeField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    time_spent = models.IntegerField()
    cards_seen = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
