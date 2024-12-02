from django.db import models

# Create your models here.
class SalesData(models.Model):
    date = models.DateField()
    product = models.CharField(max_length=20)
    sales = models.FloatField()
    region = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.date} - {self.product} ({self.region})"