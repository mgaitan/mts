===========================================
mts, miratuserie.tv on the command line
===========================================


.. image:: https://img.shields.io/pypi/v/mts.svg
   :target: https://pypi.python.org/pypi/mts
   :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/mts.svg
   :target: https://pypi.python.org/pypi/mts
   :alt: Number of PyPI downloads


`miratuserie.tv <http://miratuserie.tv>`_ is a site to stream tv shows with spanish subtitles. ``mts`` do the same, but in a geek (yonkie) way.


.. attention::

    At this moment, only episodes having a source in Pinit.tv or uptobox.com could be played.


Install
----------

::

    $ pip install mts

Usage
------

This will show the whole 3º season of *How I met your mother*::

    $ mts 'how i met' s03e01

The complete inline help looks like this::

    (mts)tin@morochita:~$ mts -h
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
      -n, --no_subtitle     Don't download subtitles
      -d, --download        Download the episode instead play it (TO DO)


Configuration
--------------

Not so much by the moment, but you can set your prefered player
in ``~/.mts/config.ini``.

By default, ``mts`` tries to use ``mplayer`` in full-screen,
with this config file::

    [main]
    player = mplayer -fs {episode} [-sub {subs}]


The substring between ``[]`` is used only if the ``-n`` (no subtitles) flag isn't present in the command line

For example, if you want to use ``vlc``, something like this should work::

    [main]
    player = vlc -f {episode} [:sub-file={subs}]

you got the idea.



* Free software: BSD license
