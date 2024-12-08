import jwt
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import User

class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request has an Authorization header
        token = request.headers.get('Authorization')

        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]  # Extract the token

            try:
                # Decode the token
                payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
                
                # Attach user to request object (optional)
                user = User.objects.filter(id=payload['id']).first()
                if user:
                    request.user = user
                else:
                    return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            except jwt.ExpiredSignatureError:
                return Response({'status': 'error', 'message': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({'status': 'error', 'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': 'error', 'message': 'Token missing or invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        # Proceed with the request
        response = self.get_response(request)
        return response
