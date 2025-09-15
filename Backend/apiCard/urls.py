from django.urls import path
from .views import (
    UserDetailView,
    CardDetailView,
    UserUpdateView,
    CardUpdateView,
    RegistrationView
)

urlpatterns = [
    # Gets
    path('user/<str:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('card/<str:card_number>/', CardDetailView.as_view(), name='card-detail'),
    
    # Updates
    path('update/user/<str:user_id>/', UserUpdateView.as_view(), name='user-update'),
    path('update/card/<str:card_number>/', CardUpdateView.as_view(), name='card-update'),
    
    # Post
    path('register/', RegistrationView.as_view(), name='register'),
]

