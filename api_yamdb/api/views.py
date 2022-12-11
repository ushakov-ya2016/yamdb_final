from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets, permissions

from api.permissions import IsAdminModeratorAuthorOrReadOnly, IsAdminOrReadOnly
from api.serializers import (
    CategorySerializer,
    CommentsSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)
from reviews.models import Category, Genre, Review, Title


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = [IsAdminOrReadOnly, ]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = TitleReadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year', )

    def get_queryset(self):
        queryset = (
            Title.objects.annotate(rating=Avg('reviews__score')).order_by('id')
        )
        filter_field = self.request.query_params
        if filter_field.get('category'):
            queryset = queryset.filter(
                category__slug=filter_field.get('category')
            )
        elif filter_field.get('genre'):
            queryset = queryset.filter(genre__slug=filter_field.get('genre'))
        elif filter_field.get('name'):
            queryset = queryset.filter(name__contains=filter_field.get('name'))
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAdminModeratorAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    ]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        ).reviews.all().order_by('id')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        )


class CommentsViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAdminModeratorAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    ]
    serializer_class = CommentsSerializer

    def get_queryset(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        ).comments.all().order_by('id')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(
                Review, pk=self.kwargs.get('review_id'),
                title=self.kwargs.get('title_id')))
