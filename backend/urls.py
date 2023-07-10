from django.urls import path
from . import views

urlpatterns = [
    path("user/<int:id>/", views.Users.as_view(), name="users" ),
]