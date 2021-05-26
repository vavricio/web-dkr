from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import AnimeCreateView, AnimeDeleteView, AnimeEditView, LoginView, RegistrationView

urlpatterns = [
    path('', AnimeCreateView.as_view(), name='an-edit'),
    path('<int:pk>/', AnimeEditView.as_view(), name='an-view'),
    path('<int:pk>/delete', AnimeDeleteView.as_view(), name='an-delete'),

    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='/'), name='logout'),
    path('register', RegistrationView.as_view(), name='registration'),
]
