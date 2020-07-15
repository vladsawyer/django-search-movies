import os
from hashlib import sha1
from django.core.paginator import Paginator


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
