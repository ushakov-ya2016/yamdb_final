from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, views, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.serializers import (
    UserSerializer,
    ConfirmationCodeSerializer,
    SignupSerializer
)
from users.models import User
from users.permission import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin, ]
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, created = User.objects.get_or_create(
        email=serializer.validated_data['email'],
        username=serializer.validated_data['username'],
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Your registration token',
        f'Код подтверждения: {confirmation_code}',
        f'{settings.DEFAULT_FROM_EMAIL}',
        [serializer.validated_data['email'], ],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


class AccessTokenView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username'],
        )
        if not default_token_generator.check_token(
            user,
            serializer.validated_data['confirmation_code']
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_token(user), status=status.HTTP_200_OK)

    @staticmethod
    def get_token(user):
        return {
            'token': str(AccessToken.for_user(user))
        }
