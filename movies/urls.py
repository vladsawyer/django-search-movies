from django.urls import path
from . import views

urlpatterns = [
    path('', views.MoviesIndexView.as_view(), name='index'),
    # ex: /movie/5/
    path('movie/<int:pk>', views.MovieDetailsView.as_view(), name='movie_detail'),
    # ex: /series/5/
    path('series/<int:pk>', views.SeriesDetailsView.as_view(), name='series_detail'),
    # ex: /member/5/
    path('member/<int:pk>', views.MemberDetailsView.as_view(), name='member'),
    # ex: list/category/sci-fi
    path('list/category/<slug:slug>', views.MoviesCategoriesList.as_view(), name='movies_category_list'),
    # ex: list/year/2010-2015
    path('list/year/<str:year>', views.MoviesCategoriesList.as_view(), name='movies_years_list'),
    # ex: list/country/usa
    path('list/country/<str:country>', views.MoviesCategoriesList.as_view(), name='movies_country_list'),
    # ex: list/popular-series
    path('list/<str:slug>', views.MoviesList.as_view(), name='movies_list'),

    path('top/<str:slug>', views.MoviesTopList.as_view(), name='movies_top_by_years'),
]
