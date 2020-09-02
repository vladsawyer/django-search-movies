from django.urls import path, include
from . import views


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', views.profile, name="accounts_profile"),
    path('accounts/profile/favorites', views.favorites, name="accounts_profile_favorites"),
    path('accounts/profile/settings', views.settings, name="accounts_profile_settings"),
]
