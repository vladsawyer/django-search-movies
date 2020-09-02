from django.shortcuts import render
from django.views.generic.base import View


class BaseProfileView:
    pass


class ProfileView(View, BaseProfileView):
    pass


profile = ProfileView.as_view()


class FavoritesView(View, BaseProfileView):
    pass


favorites = ProfileView.as_view()


class SettingsView(View, BaseProfileView):
    pass


settings = ProfileView.as_view()
