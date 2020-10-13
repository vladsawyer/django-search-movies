import json
import dateparser as dateparser
from django.core import files
import pytest
import locale
from django.core.exceptions import MultipleObjectsReturned
from movies.models import *


@pytest.mark.skip
@pytest.mark.django_db
class TestMembers:
    """testing push data to bd from json"""
    locale.setlocale(locale.LC_ALL, '')
    path = 'media/данные/person.json'
    categories = {'фэнтези': 'fantasy', 'детектив': 'detective', 'комедия': 'comedy', 'аниме': 'anime',
                  'мелодрама': 'romance', 'ужасы': 'horror', 'вестерн': 'western', 'боевик': 'action',
                  'триллер': 'thriller', 'фантастика': 'sci-fi', 'биография': 'biography', 'драма': 'drama',
                  'военный': ' military', 'мюзикл': 'musical', 'спорт': 'sports', 'криминал': 'crime',
                  'семейный': 'family', 'фильм-нуар': 'filmnoir', 'музыка': 'music', 'приключения': 'adventure',
                  'история': 'history', 'детский': 'children', 'короткометражка': 'short-film', 'мультфильм': 'cartoon',
                  'документальный': 'documentary', 'ток-шоу': 'talk-show'}
    roles = {'Продюсер', 'Актриса: Дубляж', 'Актер: Дубляж', 'Директор фильма', 'Актер', 'Актриса', 'Режиссер',
             'Оператор', 'Сценарист', 'Монтажер', 'Композитор', 'Режиссер дубляжа', 'Художник'}

    def setup(self):
        parent = Categories.objects.create(title='жанры', slug='geners', parent=None)
        for title, slug in self.categories.items():
            Categories.objects.create(
                title=title,
                slug=slug,
                parent=parent
            )

        for role in self.roles:
            Roles.objects.create(role=role)

        with open(self.path, 'r') as f:
            data = json.loads(f.read())
            for i in data[:2]:
                full_name = i.get('name')
                description = i.get('description')
                roles = i.get('roles')
                birthday = i.get('birthday')
                categories = i.get('genre')
                total_movies = i.get('total_movies')
                image_path = i.get('photo')

                if birthday is not None:
                    birthday = dateparser.parse(birthday, ['%B %Y', '%d %B Y%', '%Y'], languages=['ru']).strftime(
                        '%Y-%m-%d')

                image = open('media/данные/' + image_path, 'rb')
                name_img = image_path.split('/')[-1]
                temp_image = files.File(image, name=name_img)
                person = Members.objects.create(
                    full_name=full_name,
                    total_movies=total_movies,
                    description=description,
                    birthday=birthday,
                    image=temp_image
                )

                if roles is not None:
                    for role in roles:
                        item_role = Roles.objects.get(role=role)
                        person.roles.add(item_role)

                if categories is not None:
                    for category in categories:
                        item_category = Categories.objects.get(title=category)
                        person.categories.add(item_category)

    def test_member_get_manytomany_set(self):
        """test push data members"""
        person = Members.objects.prefetch_related().first()
        roles = [item.role for item in person.roles.all()]
        categories = [item.title for item in person.categories.all()]
        assert person.full_name == 'Мигель Хелаберт'
        assert set(roles) == {'Актер'}
        assert set(categories) == {'драма', 'триллер', 'комедия'}


@pytest.mark.skip
@pytest.mark.django_db
class TestMovie:
    path = 'media/данные/items.json'
    locale.setlocale(locale.LC_ALL, '')

    def setup(self):
        with open(self.path, 'r') as f:
            data = json.loads(f.read())
            for i in data:
                title = i.get('title')
                description = i.get('description')
                poster = i.get('poster')
                country = i.get('country')
                directors = i.get('directors')
                actors = i.get('actors')
                genres = i.get('genre')
                world_premiere = i.get('world_premier')
                rating_kp = i.get('rating_kp')
                rating_imdb = i.get('rating_imdb')
                rf_premiere = i.get('rf_premiere')
                budget = i.get('budget')
                trailer = i.get('trailer')
                fees_in_usa = i.get('fees_in_usa')
                fees_in_world = i.get('fees_in_world')
                movie_shots = i.get('movie_shots')

                if world_premiere is not None:
                    world_premiere = dateparser.parse(world_premiere, ['%B %Y', '%d %B Y%', '%Y'],
                                                      languages=['ru']).strftime('%Y-%m-%d')

                if rf_premiere is not None:
                    rf_premiere = dateparser.parse(rf_premiere, ['%B %Y', '%d %B Y%', '%Y'], languages=['ru']).strftime(
                        '%Y-%m-%d')

                movie = Movies.objects.create(
                    title=title,
                    description=description,
                    country=country,
                    world_premiere=world_premiere,
                    rating_kp=rating_kp,
                    rating_imdb=rating_imdb[0] if rating_imdb is not None else rating_imdb,
                    rf_premiere=rf_premiere,
                    budget=budget,
                    fees_in_usa=fees_in_usa,
                    fees_in_world=fees_in_world,
                    trailer=trailer[0] if trailer is not None else trailer,
                )

                if genres is not None:
                    for genre in genres:
                        if Categories.objects.filter(title=genre).exists():
                            item_genre = Categories.objects.get(title=genre)
                            movie.categories.add(item_genre)

                if poster is not None:
                    with open('media/данные/' + poster, 'rb') as ms:
                        name_poster_img = poster.split('/')[-1]
                        temp_poster_img = files.File(ms, name=name_poster_img)
                        movie.poster = temp_poster_img
                        movie.save()

                if movie_shots is not None:
                    for movie_shot in movie_shots:
                        with open('media/данные/' + movie_shot, 'rb') as ms:
                            name_movie_shot_img = movie_shot.split('/')[-1]
                            temp_movie_shot_img = files.File(ms, name=name_movie_shot_img)
                            MovieShots.objects.create(
                                image=temp_movie_shot_img,
                                movie=movie
                            )

                if Members.objects.filter(full_name=directors).exists():
                    try:
                        director = Members.objects.get(full_name=directors)
                    except MultipleObjectsReturned:
                        director = Members.objects.filter(full_name=directors)[0]
                    movie.directors.add(director)

                if actors is not None:
                    for actor in actors:
                        if Members.objects.filter(full_name=actor).exists():
                            try:
                                item_actor = Members.objects.get(full_name=actor)
                            except MultipleObjectsReturned:
                                item_actor = Members.objects.filter(full_name=actor)[0]
                            movie.actors.add(item_actor)

    def test_first_movie(self):
        """test push data members"""
        movie = Movies.objects.prefetch_related().first()
        actors = [item.full_name for item in movie.actors.all()]
        genres = [item.title for item in movie.genres.all()]
        return movie.title, actors, genres

