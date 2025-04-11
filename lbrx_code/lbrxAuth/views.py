from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import SignupSerializer, VerifyEmailSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
# from .tokens import account_activation_token  # 이메일 인증 토큰 생성 클래스 (별도 파일에 정의 필요)
from django.core.mail import send_mail
from django.conf import settings
import jwt
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            payload = {
                'user_id': user.id,
                'exp': timezone.now() + timedelta(hours=24)
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            activation_url = f"{settings.FRONTEND_URL}/activate/{token}" 

            subject = 'Activate Lbrx Account'
            message = f'Click th: {activation_url}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                return Response({'message': '회원가입이 완료되었습니다. 이메일을 확인하여 계정을 활성화하세요.'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': '이메일 전송에 실패했습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload['user_id']
                user = get_object_or_404(User, id=user_id)
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    return Response({'message': '계정이 활성화되었습니다.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': '이미 활성화된 계정입니다.'}, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return Response({'error': '만료된 토큰입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            except jwt.InvalidTokenError:
                return Response({'error': '유효하지 않은 토큰입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': '존재하지 않는 사용자입니다.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)