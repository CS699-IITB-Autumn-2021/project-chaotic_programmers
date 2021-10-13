from django.db import models

# Create your models here.
class TestModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=100, blank=True, default='')
    answer = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['created_at']