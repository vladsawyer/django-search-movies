from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl_drf.compat import StringField, KeywordField
from search.utils import html_strip, add_index_settings
from movies.models import Collection


collection_index = Index('collection')
add_index_settings(collection_index)


@collection_index.doc_type
class CollectionDocument(Document):
    """Collection Elasticsearch document."""
    id = fields.IntegerField(attr='id')
    title = StringField(
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
        }
    )
    collection_url = fields.TextField(attr='get_absolute_url')
    image = fields.FileField(attr="image")

    class Django(object):
        """Inner nested class Django."""
        model = Collection  # The model associate with this Document
