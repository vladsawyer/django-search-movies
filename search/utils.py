from elasticsearch_dsl import analyzer


html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "snowball"],
    char_filter=["html_strip"]
)


def add_index_settings(index):
    index.settings(
        number_of_shards=3,
        number_of_replicas=1
    )
