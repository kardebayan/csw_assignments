from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = 'Export content data to a JSON fixture for backup or migration.'

    def add_arguments(self, parser):
        parser.add_argument(
            'output',
            nargs='?',
            default='content_backup.json',
            help='Destination fixture path.',
        )

    def handle(self, *args, **options):
        output = options['output']
        call_command(
            'dumpdata',
            'auth.User',
            'contentApp.Article',
            'taggit.Tag',
            'taggit.TaggedItem',
            natural_foreign=True,
            natural_primary=True,
            indent=2,
            output=output,
        )
        self.stdout.write(self.style.SUCCESS(f'Exported content fixture to {output}'))
