from django.urls import path, include
from . import views


urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/', views.profile, name="accounts_profile"),
    path('profile/favorites', views.favorites, name="accounts_profile_favorites"),
    path('profile/settings', views.settings, name="accounts_profile_settings"),
]
