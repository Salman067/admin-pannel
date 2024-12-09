from rest_framework.views import APIView
from . import serializers
from . import models
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
import datetime
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from django.contrib.auth import update_session_auth_hash

@api_view(["POST"])
@permission_classes([AllowAny])
def registration(request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = models.User.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            refresh['user_type'] = user.user_type  
            refresh['id'] = user.id
            refresh['email'] = user.email
            refresh['exp'] = int((datetime.datetime.utcnow() + datetime.timedelta(minutes=30)).timestamp())
            refresh['iat'] = int(datetime.datetime.utcnow().timestamp())
            return Response({
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
                'message': 'Logged in successfully'
            })
        else:
            return Response({'status': 'error', 'message': 'Incorrect email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    except models.User.DoesNotExist:
        return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    if not user.is_authenticated:
        return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")

    if not old_password or not new_password:
        return Response({"error": "Both old and new passwords are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.check_password(old_password):
        return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

    if old_password == new_password:
        return Response({"error": "New password cannot be the same as the old password"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    update_session_auth_hash(request, user)

    return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_details(request,id=None):
    if id:
        try:
            user=models.User.objects.get(id=id)
            serializer=serializers.UserSerializer(user)
            return Response(serializer.data)
        except models.User.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    else:
        try:
            user=models.User.objects.all()
            serializer=serializers.UserSerializer(user,many=True)
            return Response(serializer.data)
        except models.User.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)    

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'status': 'success', 'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
    except TokenError as e:
        return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)