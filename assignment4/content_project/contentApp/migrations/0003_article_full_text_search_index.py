from django.db import migrations
from django.db.migrations.operations.base import Operation


class CreateArticleSearchIndex(Operation):
    reversible = True
    reduces_to_sql = True

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        if schema_editor.connection.vendor != 'postgresql':
            return

        schema_editor.execute(
            """
            CREATE INDEX IF NOT EXISTS contentapp_article_search_idx
            ON "contentApp_article"
            USING GIN (
                (
                    setweight(to_tsvector('english', coalesce("title", '')), 'A') ||
                    setweight(to_tsvector('english', coalesce("body", '')), 'B')
                )
            );
            """
        )

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        if schema_editor.connection.vendor != 'postgresql':
            return

        schema_editor.execute('DROP INDEX IF EXISTS contentapp_article_search_idx;')

    def describe(self):
        return 'Create PostgreSQL GIN index for article full-text search'


class Migration(migrations.Migration):

    dependencies = [
        ('contentApp', '0002_rename_contentapp__publish_c6c316_idx_contentapp__publish_3b1a2f_idx'),
    ]

    operations = [
        CreateArticleSearchIndex(),
    ]
