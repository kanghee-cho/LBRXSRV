from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator

User = get_user_model()

# signup
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    check_password = serializers.CharField(write_only=True)
    # Ensure email and nickname are unique
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    nickname = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())], max_length=30)

    class Meta:
        model = User
        fields = ('email', 'nickname', 'password', 'check_password')
        extra_kwargs = {
            'password': {'write_only': True},
            'check_password': {'write_only': True}
        }
    
    def validate(self, data):
        if data['password'] != data['check_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            password=validated_data['password']
        )
        return user
    
class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            # Check if the user exists and authenticate
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials", code=401)
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled", code=403)
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'", code=400)

        attrs['user'] = user
        return attrs

class LoginResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj['user']
        return {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }