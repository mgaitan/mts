import re
import requests
import subprocess
import tempfile

from django.core.management.base import BaseCommand, CommandError
from mts.orm_magic.models import Show


def get_numbers(s):
    """Extracts all integers from a string an return them in a list"""

    return map(int, re.findall(r'[0-9]+', unicode(s)))


def urlretrieve(url):
    r = requests.get(url)
    filename = tempfile.mkstemp(suffix='.srt')
    with open(filename, 'wb') as f:
        f.write(r.content)
    return filename


class Command(BaseCommand):
    args = 'show episode'

    def handle(self, *args, **options):
        show = Show.objects.filter(title__icontains=args[1])

        if show.count() == 0:
            raise CommandError('Show not found')
        elif show.count() > 1:
            raise CommandError('Show name is ambiguos')

        show = show[0]

        season, episode_number = get_numbers(args[2])

        for episode in show.episode_set.filter(season=season,
                                               episode__gte=episode_number):
            print "Retrieving %s %s..." % (show, episode.number)
            if not episode.video:
                raise CommandError('No pinit source for this episode')

            subs = urlretrieve(episode.subtitle)

            arguments = ['mplayer', '-fs', episode.video, '-sub', subs]
            subprocess.call(arguments)
