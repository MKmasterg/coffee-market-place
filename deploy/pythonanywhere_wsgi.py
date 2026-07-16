# Paste this into PythonAnywhere Web tab → WSGI file:
# /var/www/mkmsater_pythonanywhere_com_wsgi.py
#
# Adjust paths if your clone directory or virtualenv name differs.

import os
import sys

from dotenv import load_dotenv

path = '/home/mkmsater/coffee-market-place'
if path not in sys.path:
    sys.path.insert(0, path)

load_dotenv(os.path.join(path, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CoffeeMarketPlace.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
