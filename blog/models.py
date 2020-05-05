from django.db import models
from tinymce.models import HTMLField

class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    text = HTMLField(default='')
    date = models.DateField()

    def __str__(self):
        return self.title
