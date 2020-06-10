from django.core.paginator import Paginator


def get_pagination(request, queryset, count_show_list):
    paginator = Paginator(queryset, count_show_list)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return page_obj
