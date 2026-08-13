from django.urls import path

from core import views


urlpatterns = [
    path("health/", views.health, name="health"),
    path("catalogue/cards/", views.card_list, name="card-list"),
]
