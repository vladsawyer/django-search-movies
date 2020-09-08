from django.shortcuts import render
from core.views import BaseView


class ProfileView(BaseView):

    def get(self, request):
        context = {}
        return render(request=request,
                      template_name='account/profile/profile.html',
                      context=context)


profile = ProfileView.as_view()


class FavoritesView(BaseView):
    pass


favorites = ProfileView.as_view()


class SettingsView(BaseView):
    pass


settings = ProfileView.as_view()
