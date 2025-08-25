from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Kullanıcı kayıt serializer'ı"""
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }
    
    def validate_email(self, value):
        """Email benzersizliğini kontrol et"""
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("Bu email adresi zaten kullanılıyor.")
        return value.lower()
    
    def validate_username(self, value):
        """Username benzersizliğini kontrol et"""
        if User.objects.filter(username=value.lower()).exists():
            raise serializers.ValidationError("Bu kullanıcı adı zaten kullanılıyor.")
        return value.lower()
    
    def validate(self, attrs):
        """Parolaların eşleştiğini kontrol et"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Parolalar eşleşmiyor."})
        return attrs
    
    def create(self, validated_data):
        """Yeni kullanıcı oluştur"""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Kullanıcı giriş serializer'ı"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            # Email ile kullanıcıyı bul
            try:
                user = User.objects.get(email=email.lower())
                username = user.username
            except User.DoesNotExist:
                raise serializers.ValidationError("Geçersiz giriş bilgileri.")
            
            # Kullanıcı adı ile authenticate et
            user = authenticate(username=username, password=password)
            
            if not user:
                raise serializers.ValidationError("Geçersiz giriş bilgileri.")
            
            if not user.is_active:
                raise serializers.ValidationError("Hesap devre dışı bırakılmış.")
                
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("Email ve parola gerekli.")


class UserSerializer(serializers.ModelSerializer):
    """Kullanıcı bilgi serializer'ı"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_active')
        read_only_fields = ('id', 'username', 'date_joined', 'is_active')
