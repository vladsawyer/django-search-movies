from django.urls import path, include
from . import views


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', views.profile, name="accounts_profile"),
    path('accounts/profile/', views.favorites, name="accounts_profile_favorites"),
    path('accounts/profile/', views.settings, name="accounts_profile_settings"),
]
