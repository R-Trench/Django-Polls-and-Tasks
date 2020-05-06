from django.db import models
from tinymce.models import HTMLField

class Blog(models.Model):
    title = models.CharField(max_length=200)
    # came in later to add this field so it needed a default value for pre-existing items.
    text = HTMLField(default='')
    date = models.DateField()

    def __str__(self):
        return self.title
