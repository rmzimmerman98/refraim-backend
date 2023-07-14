from django.urls import path
from . import views

urlpatterns = [
    path("user/<int:id>/", views.Users.as_view(), name="users" ),
    path("register/", views.RegisterView.as_view(), name="registerShow"),
    path('token/', views.TokenView.as_view(), name="token_obtain_pair"),
    path('allconversations/<int:id>/', views.Conversations.as_view(), name="allconversations"),
    path('allconversations/<int:id>/favorites/', views.Favorites.as_view(), name="favorites"),
    path('conversation/<int:id>/', views.ConversationShow.as_view(), name="conversationshow"),
    path('googlelogin/', views.GoogleLoginView.as_view(), name="googlelogin"),
]