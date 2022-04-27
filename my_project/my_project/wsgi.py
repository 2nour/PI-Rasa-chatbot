"""
WSGI config for my_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '   my_project.settings')
sys.path.append('/home/django_projects/my_project')
sys.path.append('/home/django_projects/my_project/my_project')


application = get_wsgi_application()
