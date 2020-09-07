from django.urls import path, include
from . import views


list_urlpatterns = [
    # ex: list/category/sci-fi
    path('movie/category/<slug:slug>/', views.MoviesByGenreView.as_view(), name='movies_genre_list'),
    # ex: list/year/2010-2015
    path('movie/year/<str:year>/', views.MoviesByYearView.as_view(), name='movies_years_list'),
    # ex: list/country/usa
    path('movie/country/<str:country>/', views.MoviesByCountryView.as_view(), name='movies_country_list'),

    path('popular-series/', views.PopularSeriesView.as_view(), name='popular-series'),
    path('future-premieres/', views.FuturePremieresView.as_view(), name='future-premieres'),
    path('expected-movies/', views.ExpectedMoviesView.as_view(), name='expected-movies'),
    path('recent-premieres/', views.RecentPremieresView.as_view(), name='recent-premieres'),
    path('popular-movies/', views.PopularMoviesView.as_view(), name='popular-movies'),
    path('interesting-today/', views.InterestingTodayView.as_view(), name='interesting-today'),
    path('new-movies-series/', views.NewMoviesSeriesView.as_view(), name='new-movies-series'),
    path('movies-month/', views.MoviesMonthView.as_view(), name='movies-month'),
]

top_urlpatterns = [
    path('russian-classics/', views.RussianClassicsView.as_view(), name='russian-classics'),
    path('foreign-classics/', views.ForeignClassicsView.as_view(), name='foreign-classics'),
    path('by-rating-kp/', views.ByRatingKinopoiskView.as_view(), name='by-rating-kp'),
    path('by-rating-imdb/', views.ByRatingImdbView.as_view(), name='by-rating-imdb'),
    path('cartoon/', views.ByRatingImdbView.as_view(), name='cartoon'),
]

comment_urlpatterns = [
    # ex:comment/movie/722
    path('movie/<int:pk>', views.add_comment_to_movie, name='movie_comment'),
]

vote_urlpatterns = [
    path('comment/<int:pk>/like', views.add_like_to_comment, name='comment_like'),
    path('comment/<int:pk>/dislike', views.add_dislike_to_comment, name='comment_dislike'),
    path('movie/<int:pk>/like', views.add_like_to_movie, name='movie_like'),
    path('movie/<int:pk>/dislike', views.add_dislike_to_movie, name='movie_dislike'),

]

urlpatterns = [
    path('', views.MoviesIndexView.as_view(), name='index'),
    # ex: /movie/5/
    path('movie/<int:pk>', views.MovieDetailsView.as_view(), name='movie_detail'),
    # ex: /series/5/
    path('series/<int:pk>', views.SeriesDetailsView.as_view(), name='series_detail'),
    # ex: /member/5/
    path('member/<int:pk>', views.MemberDetailsView.as_view(), name='member'),

    # ajax vote
    path('', include(vote_urlpatterns)),

    path('comment/', include(comment_urlpatterns)),
    path('list/', include(list_urlpatterns)),
    path('top/', include(top_urlpatterns)),

    path("filter/countries/", views.get_filter_countries, name='get_countries'),
    path("filter/years/", views.get_filter_year, name='get_years'),
    path("filter/genres/", views.get_filter_genres, name='get_genres'),
    path("filter/categories/", views.get_filter_categories, name='get_categories'),
]
