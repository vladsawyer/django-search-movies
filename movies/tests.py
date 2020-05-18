import json

import dateparser as dateparser
from django.core import files
import pytest
import locale
from datetime import datetime
from movies.models import *


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestMembers:
    """testing push data to bd from json"""
    pytestmark = pytest.mark.django_db
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
                    birthday = dateparser.parse(birthday, ['%B %Y', '%d %B Y%', '%Y'], languages=['ru']).strftime('%Y-%m-%d')

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
