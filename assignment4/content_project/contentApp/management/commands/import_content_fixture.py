from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = 'Import content data from a JSON fixture.'

    def add_arguments(self, parser):
        parser.add_argument('fixture', help='Fixture path to load.')

    def handle(self, *args, **options):
        fixture = options['fixture']
        call_command('loaddata', fixture)
        self.stdout.write(self.style.SUCCESS(f'Imported content fixture from {fixture}'))
