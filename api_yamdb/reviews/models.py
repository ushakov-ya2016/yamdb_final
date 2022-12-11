from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from reviews.validators import validate_year


class Category(models.Model):
    """
    Категории (типы) произведений.
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Категория произведения'
        verbose_name_plural = 'Категории произведений'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Жанры произведений.
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы.
    """
    name = models.CharField(max_length=256)
    year = models.IntegerField(
        validators=[
            MinValueValidator(1, 'Год должен быть от 1 до текущего'),
            validate_year,
        ]
    )
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='categories')
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['pk']

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """
    Модель для связи жанров и произведений.
    """
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Связь произведения и жанра'
        verbose_name_plural = 'Связь произведений и жанров'
        ordering = ['title']

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    """
    Модель для создания отзывов.
    """
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(
        verbose_name='Оценка произведения',
        validators=[
            MinValueValidator(1, 'Оценка должна быть целым числом от 1 до 10'),
            MaxValueValidator(10, 'Оценка должна быть целым числом от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pk']

        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]


class Comments(models.Model):
    """
    Модель для создания комментариев к отызвам.
    """
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pk']
