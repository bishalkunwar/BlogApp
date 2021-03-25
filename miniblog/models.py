from django.db import models

# Create your models here.
#database codes:

class post(models.Model):
    title = models.CharField(max_length=50)
    desc = models.TextField()
