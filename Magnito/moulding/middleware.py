from urllib.parse import quote

from django.conf import settings
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    """Middleware that requires a user to be authenticated to view any page

    Exemptions: any path that starts with the prefixes in `whitelist_prefixes`.
    If the user is not authenticated and no company session exists, they are
    redirected to the site root (login landing page) with a `next` query
    parameter.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Paths that do not require login
        # Normalize static/media prefixes to start with '/'
        static_prefix = settings.STATIC_URL if settings.STATIC_URL.startswith('/') else f"/{settings.STATIC_URL.lstrip('/') if settings.STATIC_URL else ''}"
        media_prefix = settings.MEDIA_URL if settings.MEDIA_URL.startswith('/') else f"/{settings.MEDIA_URL.lstrip('/') if settings.MEDIA_URL else ''}"

        self.whitelist_prefixes = [
            '/auth/',
            '/admin/',
            static_prefix,
            media_prefix,
            '/favicon.ico',
        ]

    def __call__(self, request):
        path = request.path_info or '/'

        # Allow the site root (login landing page) and whitelisted prefixes
        # (root must be allowed so unauthenticated users can reach the login page)
        if path == '/' or path == '':
            return self.get_response(request)

        # Allow whitelisted prefixes
        for prefix in self.whitelist_prefixes:
            if prefix and path.startswith(prefix):
                return self.get_response(request)

        # Allow if Django user is authenticated or a company session exists
        if request.user.is_authenticated or request.session.get('company_id'):
            return self.get_response(request)

        # Not authenticated -> redirect to the whitelisted auth root with next
        # Using /auth/ prevents redirect loops because /auth/ is whitelisted above
        next_param = quote(path)
        login_url = f"/auth/?next={next_param}"
        return redirect(login_url)
