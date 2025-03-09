from django.urls import path
from .exhausts_view import (
    ExhaustCreateView, ExhaustDeleteView, ExhaustDetailView,
    ExhaustListView, ExhaustUpdateView, ExhaustQueryMarkListView
)

urlpatterns = [
    path("", ExhaustListView.as_view(), name="exhaust_list"),
    path("create/", ExhaustCreateView.as_view(), name="exhaust_create"),
    path("<int:id>/", ExhaustDetailView.as_view(), name="exhaust_detail"),
    path("<int:id>/update/", ExhaustUpdateView.as_view(), name="exhaust_update"),
    path("<int:id>/delete/", ExhaustDeleteView.as_view(), name="exhaust_delete"),
    path("<int:exhaust_mark_id>/marca_de_escapamento/", ExhaustQueryMarkListView.as_view(), name="exhaust_query_mark_list"),
]
