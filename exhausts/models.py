from django.db import models
   
class Exhausts(models.Model):
    part = models.CharField(max_length=255, null=False)
    quantity = models.IntegerField()
    
    
class CarModel(models.Model):
    name = models.CharField(max_length=255, null=False)
    year = models.CharField(max_length=10, null=False)
    

class ExhaustsCarModel(models.Model):
    exhaust = models.ForeignKey(Exhausts, on_delete=models.CASCADE, null=False)
    car_model = models.ForeignKey(CarModel, on_delete=models.RESTRICT, null=False)
