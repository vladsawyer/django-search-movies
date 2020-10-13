from django_elasticsearch_dsl import Document, Index, fields
from search.utils import html_strip, add_index_settings
from movies.models import Members
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField

member_index = Index('member')
add_index_settings(member_index)


@member_index.doc_type
class MemberDocument(Document):
    """Member Elasticsearch document."""
    id = fields.IntegerField(attr='id')
    full_name = StringField(
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )
    birthday = fields.DateField()
    roles = fields.NestedField(properties={
        'title': fields.TextField(
            analyzer=html_strip,
            attr='role',
            fields={
                'raw': KeywordField(),
            }
        ),
    })
    member_url = fields.TextField(attr='get_absolute_url')
    image = fields.FileField(attr="image")

    class Django(object):
        """Inner nested class Django."""

        model = Members  # The model associate with this Document
