import jwt
from datetime import datetime, timezone
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_access_token(user):
    """Access token oluşturur"""
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.now(timezone.utc) + settings.JWT_ACCESS_TOKEN_LIFETIME,
        'iat': datetime.now(timezone.utc),
        'type': 'access'
    }
    
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def generate_refresh_token(user):
    """Refresh token oluşturur"""
    payload = {
        'user_id': user.id,
        'exp': datetime.now(timezone.utc) + settings.JWT_REFRESH_TOKEN_LIFETIME,
        'iat': datetime.now(timezone.utc),
        'type': 'refresh'
    }
    
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_token(token):
    """Token'ı doğrular"""
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Token süresi dolmuş')
    except jwt.InvalidTokenError:
        raise ValueError('Geçersiz token')
