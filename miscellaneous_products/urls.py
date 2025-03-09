from django.urls import path
from .views import (
    MiscellaneousProductsCreateView, MiscellaneousProductsDeleteView, MiscellaneousProductsDetailView,
    MiscellaneousProductsListView, MiscellaneousProductsUpdateView
)


urlpatterns = [
    path("", MiscellaneousProductsListView.as_view(), name="miscellaneous_products_list"),
    path("<int:id>/", MiscellaneousProductsDetailView.as_view(), name="miscellaneous_products_detail"),
    path("create/", MiscellaneousProductsCreateView.as_view(), name="miscellaneous_products_create"),
    path("<int:id>/update/", MiscellaneousProductsUpdateView.as_view(), name="miscellaneous_products_update"),
    path("<int:id>/delete/", MiscellaneousProductsDeleteView.as_view(), name="miscellaneous_products_delete"),
]
