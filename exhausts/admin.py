from django.contrib import admin
from .models import Exhausts, ExhaustsCarModel, CarModel

# Registra os modelos 
admin.site.register(ExhaustsCarModel)
admin.site.register(Exhausts)
admin.site.register(CarModel)