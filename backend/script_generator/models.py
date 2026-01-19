from django.db import models

# Create your models here.
class Script(models.Model):
    title = models.CharField(max_length=100)
    context = models.TextField(max_length=1000)
    category = models.CharField(max_length=100)
    video_length = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title