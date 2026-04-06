from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_urls = [
            reverse('root'),
            reverse('login'),
            reverse('signup'),
            reverse('password_reset'),
            reverse('password_reset_done'),
        ]

        # allow reset confirm URLs like /reset/uid/token/
        allowed_prefixes = [
            '/reset/',
            '/admin/',
            '/static/',
            '/media/',
        ]

        if not request.user.is_authenticated:
            if request.path not in allowed_urls and not any(request.path.startswith(prefix) for prefix in allowed_prefixes):
                return redirect('login')

        return self.get_response(request)