#!/usr/bin/env python
import os
import sys

# Test run without Apache:
# python manage.py runserver localhost:8080

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webconf.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
