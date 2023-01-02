from django.db import models

# Create your models here.
class PDFFile(models.Model):
    filename = models.CharField(max_length=500)
    summary = models.CharField(max_length=5000000)
