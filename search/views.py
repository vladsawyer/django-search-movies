from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_EXCLUDE,
    SUGGESTER_COMPLETION,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from search.documents import (
    movie,
    member,
    collection
)
from search import serializers


class SearchMovieViewSet(DocumentViewSet):
    document = movie.MovieDocument
    serializer_class = serializers.MovieDocumentSerializer
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SuggesterFilterBackend
    ]

    # Define filter fields
    filter_fields = {
        'country': 'country.raw',
        'world_premiere': {
            'field': 'world_premiere__year',
            'lookup': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ]
        },
        'category': {
            'field': 'categories',
            # Note, that we limit the lookups of `categories` field in
            # this example, to `terms, `prefix`, `wildcard`, `in` and
            # `exclude` filters.
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
    }

    ordering_fields = {
        '_score': '_score',
        'title': 'title.raw',
        'world_premiere': 'world_premiere__year',
    }

    suggester_fields = {
        'title': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
            'options': {
                'size': 5,  # Override default number of suggestions
            },
        },

    }


class SearchMemberViewSet(DocumentViewSet):
    document = member.MemberDocument
    serializer_class = serializers.MemberDocumentSerializer
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SuggesterFilterBackend,
    ]

    filter_fields = {
        'birthday': 'birthday__year',
        'roles': 'roles__role',
    }
    ordering_fields = {
        '_score': '_score',
        'birthday': 'birthday__year',
    }

    suggester_fields = {
        'full_name': {
            'field': 'full_name.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
            'options': {
                'size': 5,  # Override default number of suggestions
            },
        },
    }


class SearchCollectionViewSet(DocumentViewSet):
    document = collection.CollectionDocument
    serializer_class = serializers.CollectionDocumentSerializer
    lookup_field = 'id'
    filter_backends = [
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SuggesterFilterBackend,
    ]

    ordering_fields = {
        'title': 'title.raw',
    }

    suggester_fields = {
        'title': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
            'options': {
                'size': 5,  # Override default number of suggestions
            },
        },
    }

