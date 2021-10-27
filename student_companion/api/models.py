from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender = settings.AUTH_USER_MODEL)

# Reference: https://www.django-rest-framework.org/api-guide/authentication/
def create_auth_token(sender, instance = None, created = False, **kwargs):
    """
        Description:
            Every user to have an automatically generated Token

        Arguments:
            sender- information of the sender (sender object)

        Returns:
            Nothing
        """
    if created:
        Token.objects.create(user = instance)


class ScUser(AbstractUser):
    """
        Description:
            Class for customizing authentication model
    """
    relations = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True)


class FlashDeck(models.Model):
    """
        Description:
            Model for decks
    """
    title = models.CharField(max_length=100, blank=False, default='')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        """
        Description:
            Mentions ordering
        """
        ordering= ['title']


class Flashcard(models.Model):
    """
        Description:
            Model for flashcards that contains flashcard details and its accountability
    """
    title = models.CharField(max_length=100, blank = False, default='')
    question = models.CharField(max_length=100, blank = False, default='')
    answer = models.CharField(max_length=100, blank = False, default='')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flash_deck = models.ForeignKey(FlashDeck, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    next_scheduled_at = models.DateTimeField(auto_now_add=True)


class FlashcardUser(models.Model):
    """
        Description:
            Model that Saves history of revisions for every flashcard per user
    """
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_opened = models.DateTimeField(blank = True, null= True)
    last_time_taken = models.IntegerField(blank = True, null = True,default=300)
    next_scheduled_at = models.DateTimeField(blank = True, null= True)
    status = models.CharField(max_length=10, blank = False, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class FlashDeckUser(models.Model):
    """
        Description:
            Model for dmapping of decks and users
    """
    flashdeck = models.ForeignKey(FlashDeck, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class ActivityMonitor(models.Model):
    """
        Description:
            Model that holds statistics of revision and time taken for every logged-in instance
    """
    date = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_spent = models.IntegerField(default=0)
    cards_seen = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)