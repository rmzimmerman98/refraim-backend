from django.urls import path
from . import views

urlpatterns = [
    path("user/<int:id>/", views.Users.as_view(), name="users" ),
    path("register/", views.RegisterView.as_view(), name="registerShow"),
    path('token/', views.TokenView.as_view(), name="token_obtain_pair"),
    path('allconversations/<int:id>/', views.Conversations.as_view(), name="allconversations"),
]