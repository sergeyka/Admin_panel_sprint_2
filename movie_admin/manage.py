#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from os import getenv

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

load_dotenv()


def main():
    """Run administrative tasks."""

    # Starting with manage.py will load development settings in config/settings/dev.py
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
