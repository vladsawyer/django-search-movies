import os
from hashlib import sha1
import random
from django.core.paginator import Paginator
from search_movies.settings import BASE_DIR


def get_pagination(request, queryset, count_show_list):
    paginator = Paginator(queryset, count_show_list)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def get_hashed_path(instance, filename) -> str:
    """
    create image, file path for ImageField and FileField in models
    example: movie_shots/b3/6d/b36d70c244cbc1858e3afa474ad279ace31dd518.jpg
    :param instance:
    :param filename:
    :return: path
    """
    hashname = sha1(filename.encode('utf-8')).hexdigest() + '.jpg'
    return os.path.join(hashname[:2], hashname[2:4], hashname)


def get_random_default_user_avatar():
    avatars = ['46035.jpg', '97365.jpg', '98137.jpg', '115127.jpg',
               '127889.jpg', '154693.jpg', '175680.jpg', '204154.jpg']

    return os.path.join(BASE_DIR, 'accounts/static/account/img', random.choice(avatars))
