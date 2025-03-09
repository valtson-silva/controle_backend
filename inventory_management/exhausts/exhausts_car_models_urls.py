from django.urls import path
from .exhausts_car_models_view import (
    ExhaustsCarModelCreateView, ExhaustsCarModelListView, ExhaustsCarModelUpdateView, ExhaustsCarListView
)

urlpatterns = [
    path("", ExhaustsCarListView.as_view(), name="exhausts_car_list"),
    path("<int:car_model_id>/", ExhaustsCarModelListView.as_view(), name="exhausts_car_model_list"),
    path("create/", ExhaustsCarModelCreateView.as_view(), name="exhausts_car_model_create"),
    path("<int:id>/update/", ExhaustsCarModelUpdateView.as_view(), name="exhausts_car_model_update"),
]
