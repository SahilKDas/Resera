from django.conf import settings
from django.http import HttpResponse


class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get("Origin")
        response = HttpResponse(status=204) if request.method == "OPTIONS" else self.get_response(request)
        if origin and origin in settings.CORS_ALLOWED_ORIGINS:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Headers"] = "Content-Type, X-CSRFToken"
            response["Access-Control-Allow-Methods"] = "GET, POST, PATCH, OPTIONS"
            response["Vary"] = "Origin"
        return response
