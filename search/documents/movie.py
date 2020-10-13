from django_elasticsearch_dsl import Document, Index, fields
from search.utils import html_strip, add_index_settings
from movies.models import Movies
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField


movie_index = Index('movie')
add_index_settings(movie_index)


@movie_index.doc_type
class MovieDocument(Document):
    """Movie Elasticsearch document."""

    id = fields.IntegerField(attr='id')
    title = StringField(
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
        }
    )
    world_premiere = fields.DateField()
    country = StringField(
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
        }
    )
    rf_premiere = fields.DateField()
    categories = fields.NestedField(properties={
        'title': fields.TextField(analyzer=html_strip),
    })
    rating_kp = fields.FloatField()
    rating_imdb = fields.FloatField()
    directors = fields.NestedField(properties={
        'full_name': fields.TextField(analyzer=html_strip),
        'id': fields.IntegerField(),
    })
    image = fields.FileField(attr="poster")
    movie_url = fields.TextField(attr='get_absolute_url')

    class Django(object):
        """Inner nested class Django."""
        model = Movies  # The model associate with this Document
