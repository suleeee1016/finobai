from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from .utils import generate_access_token, generate_refresh_token, verify_token

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Kullanıcı kayıt API endpoint'i"""
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # JWT token'ları oluştur
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        
        return Response({
            'message': 'Hesap başarıyla oluşturuldu',
            'user': UserSerializer(user).data,
            'tokens': {
                'access': access_token,
                'refresh': refresh_token
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Kullanıcı giriş API endpoint'i"""
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # JWT token'ları oluştur
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        
        return Response({
            'message': 'Giriş başarılı',
            'user': UserSerializer(user).data,
            'tokens': {
                'access': access_token,
                'refresh': refresh_token
            }
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Kullanıcı çıkış API endpoint'i"""
    # Token blacklist işlemi burada yapılabilir (gelişmiş özellik)
    return Response({
        'message': 'Başarıyla çıkış yapıldı'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Kullanıcı profil bilgileri"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Kullanıcı profil güncelleme"""
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profil başarıyla güncellendi',
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """Refresh token ile yeni access token al"""
    refresh = request.data.get('refresh_token')
    
    if not refresh:
        return Response({
            'error': 'Refresh token gerekli'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        payload = verify_token(refresh)
        
        if payload.get('type') != 'refresh':
            return Response({
                'error': 'Geçersiz token tipi'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(id=payload['user_id'])
        new_access_token = generate_access_token(user)
        
        return Response({
            'access_token': new_access_token
        }, status=status.HTTP_200_OK)
        
    except (ValueError, User.DoesNotExist):
        return Response({
            'error': 'Geçersiz refresh token'
        }, status=status.HTTP_401_UNAUTHORIZED)
