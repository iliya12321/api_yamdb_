import random

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters, mixins, viewsets, status

from api.permissions import (
    IsAuthorModerAdminOrReadOnly,
    IsAdmin,
    IsAdminOrReadOnly,
)

from reviews.models import Review, Title, Category, Genre, User
from api.serializers import (
    CommentSerializer,
    ReviewSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    UserSerializer,
    UserMeSerializer,
    SignUpSerializer,
    GetTokenSerializer,
    TitleCreateAndUpdateSerializer
)
from .filters import TitleFilter


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModerAdminOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModerAdminOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class GetPostDelete(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(GetPostDelete):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class GenreViewSet(GetPostDelete):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateAndUpdateSerializer
        return TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'


class APIUserMe(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserMeSerializer(
            user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APISignUp(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')

        if not User.objects.filter(
            username=username,
            email=email
        ).exists():
            serializer = SignUpSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(username=username)
                confirmation_code = user.confirmation_code
                message = (
                    f'Ваш код: {confirmation_code}\n'
                    'Перейдите по адресу '
                    'http://127.0.0.1:8000/api/v1/auth/token/ и введите его '
                    'вместе со своим username'
                )
                send_mail(
                    'Завершение регистрации',
                    message,
                    'webmaster@localhost',
                    [email, ],
                    fail_silently=True
                )
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            user = User.objects.get(username=username)
            user.confirmation_code = random.randint(10000, 99999)
            user.save()
            message = (
                f'Ваш код: {user.confirmation_code}\n'
                'Перейдите по адресу '
                'http://127.0.0.1:8000/api/v1/auth/token и введите его '
                'вместе со своим username'
            )
            send_mail(
                'Завершение регистрации',
                message,
                'webmaster@localhost',
                [email, ],
                fail_silently=True
            )
            return Response(
                {
                    'username': username,
                    'email': email
                },
                status=status.HTTP_200_OK
            )


class APIGetToken(APIView):
    def post(self, request):

        username = request.data.get('username')
        serializer = GetTokenSerializer(data=request.data)

        if not User.objects.filter(
            username=username
        ).exists():
            if serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.get(username=username)
        if request.data.get('confirmation_code') != user.confirmation_code:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

        access = AccessToken.for_user(user)
        return Response(
            {
                'token': f'Bearer {access}',
            },
            status=status.HTTP_200_OK
        )
