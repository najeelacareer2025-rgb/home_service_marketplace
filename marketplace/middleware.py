from django.contrib import messages
from django.conf import settings

class LoginRequiredMessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path not in [settings.LOGIN_URL, '/register/']:
            if 'next=' in request.get_full_path():
                messages.info(request, "Please log in to continue.")
        return self.get_response(request)
