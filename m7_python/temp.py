import os
import django
from decouple import config

import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import mysite
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()












