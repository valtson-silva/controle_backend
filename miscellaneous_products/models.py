from django.db import models

class MiscellaneousProducts(models.Model):
    name = models.CharField(max_length=255, null=False)
    quantity = models.IntegerField()
