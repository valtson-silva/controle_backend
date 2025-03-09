from django.urls import path
from .car_model_view import (
    CarModelCreateView, CarModelDeleteView, CarModelDetailView,
    CarModelListView, CarModelUpdateView
)

urlpatterns = [
    path("", CarModelListView.as_view(), name="car_model_list"),
    path("create/", CarModelCreateView.as_view(), name="car_model_create"),
    path("<int:id>/", CarModelDetailView.as_view(), name="car_model_detail"),
    path("<int:id>/update/", CarModelUpdateView.as_view(), name="car_model_update"),
    path("<int:id>/delete/", CarModelDeleteView.as_view(), name="car_model_delete"),
]
