
def shell():
    import os, sys

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mts.settings")

    from django.core.management import call_command
    call_command('mts_cli', *sys.argv)