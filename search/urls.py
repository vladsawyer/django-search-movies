from . import views
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
movie = router.register(r'movie', views.SearchMovieViewSet, basename='search_movie')
member = router.register(r'member', views.SearchMemberViewSet, basename='search_member')
collection = router.register(r'collection', views.SearchCollectionViewSet, basename='search_collection')


urlpatterns = [
    url(r'^', include(router.urls)),
]
