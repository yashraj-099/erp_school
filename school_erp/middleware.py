import requests
import time
from django.conf import settings
from django.http import JsonResponse
from django.core.cache import cache
from django.urls import resolve

class CASJWTAuthenticationMiddleware:
    """
    Middleware that verifies JWT tokens with CAS.
    - Verifies via CAS_VERIFY_ENDPOINT (POST /api/tokens/verify/)
    - Attaches user + platform info to request.cas_user and request.cas_permissions
    - Skips validation for whitelisted/public URLs
    - Optionally caches verification results for performance
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 👇 Step 1: Skip middleware for public URLs (e.g. login, static, media)
        public_paths = [
            '/login/', '/logout/', '/register/',
            '/admin/', '/static/', '/media/',
        ]
        if any(request.path.startswith(p) for p in public_paths):
            return self.get_response(request)

        # 👇 Step 2: Extract Bearer token
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            request.cas_user = None
            return self.get_response(request)

        # 👇 Step 3: Check if token is cached and valid
        cached_data = cache.get(f"cas_token_{token}")
        if cached_data:
            request.cas_user = cached_data["user"]
            request.cas_permissions = cached_data["platforms"]
            return self.get_response(request)

        # 👇 Step 4: Validate token with CAS
        try:
            response = requests.post(
                settings.CAS_VERIFY_ENDPOINT,
                json={"token": token},
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('valid'):
                    # Attach CAS user info
                    request.cas_user = data['user']
                    request.cas_permissions = data.get('platforms', [])

                    # ✅ Cache result for 2 minutes
                    cache.set(f"cas_token_{token}", data, timeout=120)
                else:
                    return JsonResponse({'detail': 'Invalid CAS token'}, status=401)
            else:
                return JsonResponse({'detail': 'CAS verification error'}, status=response.status_code)

        except requests.exceptions.RequestException as e:
            return JsonResponse({'detail': 'CAS connection failed', 'error': str(e)}, status=503)

        # 👇 Step 5: Continue normal flow
        response = self.get_response(request)
        return response
