"""
ASGI config for injection_moulding project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'injection_moulding.settings')

application = get_asgi_application()
