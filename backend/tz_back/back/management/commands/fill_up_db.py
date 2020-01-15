import json
from os.path import join
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings

from back import models as m


class Command(BaseCommand):
    help = 'Fill up db'

    USER_JSON_FILE_NAME = 'users.json'
    USER_STATISTIC_JSON_FILE_NAME = 'users_statistic.json'

    def get_file_path(self, file_name):
        dir_path = Path(settings.CONFIG_ROOT).parent
        self.stdout.write(self.style.SUCCESS(dir_path))
        return join(dir_path, file_name)

    @staticmethod
    def str_to_list(string_):
        return json.loads(string_)

    def fill_up_db(self, model, file_name):
        with open(self.get_file_path(file_name)) as f:
            statistics = self.str_to_list(f.read())
            for stat in statistics:
                instance, created = model.objects.get_or_create(**stat)
                verb = 'created' if created else 'received'
                self.stdout.write(self.style.SUCCESS(
                    f'{instance} {instance.id} successfully {verb}')
                )

    def handle(self, *args, **options):
        self.fill_up_db(m.User, self.USER_JSON_FILE_NAME)
        self.fill_up_db(m.UserStatistics, self.USER_STATISTIC_JSON_FILE_NAME)

