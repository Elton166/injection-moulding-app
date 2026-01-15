"""
WSGI config for injection_moulding project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'injection_moulding.settings')

application = get_wsgi_application()
