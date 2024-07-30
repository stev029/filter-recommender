from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model

from cfehome import utils as cfehome_utils
from movies.models import Movie

User = get_user_model()

class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('count', nargs='?', default=10, type=int)
        parser.add_argument('--movies', action='store_true', default=False)
        parser.add_argument('--users', action='store_true', default=False)
        parser.add_argument('--show-total', action='store_true', default=False)

    def handle(self, *args: Any, **options: Any) -> str | None:
        count = options.get('count')
        show_total = options.get('show_total')
        load_movies = options.get('movies')
        generate_users = options.get('users')

        if load_movies:
            movie_dataset = cfehome_utils.load_movie_data(limit=count)
            movies_new = [Movie(**x) for x in movie_dataset]
            movies_bulk = Movie.objects.bulk_create(movies_new, ignore_conflicts=True)
            print('New movies: %d' % len(movies_bulk))

            if show_total:
                print('Total movies: %d' % Movie.objects.count())

        if generate_users:
            profiles = cfehome_utils.get_fake_profiles(count=count) # type: ignore
            new_users = []

            for profile in profiles:
                new_users.append(User(**profile))

            user_bulk = User.objects.bulk_create(new_users, ignore_conflicts=True)
            print('New users created %d' % len(user_bulk))

            if show_total:
                print('Total users: %d' % User.objects.count())