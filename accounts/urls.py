from django.urls import path, include
from .views import RegisterView, LogoutView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('login/', LoginView.as_view(), name='login'),
]

