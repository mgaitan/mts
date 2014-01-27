"""
mts -- miratuserie.tv in your command line

Usage:
    mts [-i] [-ns] [-d] <show> <start>
    mts -i


Arguments:
  title                 Looks for a show. Like 'how i met' or 'big bang'

  start                 Specifies a season/episode of a show to start play.
                        Examples: S01 (a whole season), s02e04 or 9x13

optional arguments:
  -i, --info            Show info about available shows and episodes
  -h, --help            Show this help message and exit
  -ns, --no_subtitle    Don't download subtitles (TO DO)
  -d, --download        Download the episode instead play it (TO DO)
"""

import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mts.settings")


import re
import subprocess
import tempfile

import requests
from docopt import docopt

from mts.orm_magic.models import Show


def get_numbers(s):
    """Extracts all integers from a string an return them in a list"""

    result = map(int, re.findall(r'[0-9]+', unicode(s)))
    return result + [1] * (2 - len(result))


def urlretrieve(url):
    r = requests.get(url)
    _, filename = tempfile.mkstemp(suffix='.srt')
    with open(filename, 'wb') as f:
        f.write(r.content)
    return filename


def main():
    args = docopt(__doc__)

    if args['--info'] and args['<show>'] is None:
        print("Available shows:\n")
        for s in Show.objects.all():
            print(s)
        return

    show = Show.objects.filter(title__icontains=args['<show>'])


    if show.count() == 0:
        sys.exit('Show not found')
    elif show.count() > 1:
        multi = '\n'.join(map(str, show))
        sys.exit('Show name is ambiguos: \n\n%s' % multi)

    show = show[0]

    season, episode_number = get_numbers(args['<start>'])


    for i, episode in enumerate(show.episode_set.filter(season=season,
                                           episode__gte=episode_number)):

        try:
            if args['--info'] and i == 0:
                title = repr(episode)[1:-1]
                print(title)
                print('-' * len(title))
                print('')
                print(episode.overview)
                return

            print("Retrieving %s %s..." % (show, episode.number))
            if not episode.video:
                sys.exit('No pinit source for this episode')

            subs = urlretrieve(episode.subtitle)

            arguments = ['mplayer', '-fs', episode.video, '-sub', subs]
            subprocess.call(arguments)
        except KeyboardInterrupt:
            sys.exit('Ok\. See you!')




if __name__ == '__main__':
    main()