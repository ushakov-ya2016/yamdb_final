from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Category, Comments, Genre, GenreTitle, Review, Title
from users.models import User

FILE_PATH = 'static/data/'

MODELS = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    User: 'users.csv',
    Review: 'review.csv',
    Comments: 'comments.csv',
}

DONE_MESSAGE = """
 - Загрузка тестовых данных завершена.
"""
ERROR_MESSAGE = """
 - Cначала нужно удалить файл "db.sqlite3" (уничтожить текущую БД)
 - Выполнить команду "python manage.py makemigrations" (создание зависимостей)
 - Выполнить команду "python manage.py migrate" (создание новых таблиц)
 - Выполнить команду "python manage.py import_csv" (загрузка тестовых данных)
 """


class Command(BaseCommand):
    help = "Загрузка тестовых данных из CSV фалов /api_yamdb/static/data/"

    def handle(self, *args, **options):
        """
        Импортирует тестовые данные из таблиц CSV в БД.
        """
        for model, csv in MODELS.items():
            if model.objects.exists():
                return self.stdout.write(self.style.WARNING(ERROR_MESSAGE))

        for row in DictReader(open(FILE_PATH + MODELS[Category],
                              encoding='utf-8')):
            Category.objects.bulk_create([
                Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
            ])

        for row in DictReader(open(FILE_PATH + MODELS[Genre],
                              encoding='utf-8')):
            Genre.objects.bulk_create([
                Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
            ])

        for row in DictReader(open(FILE_PATH + MODELS[Title],
                              encoding='utf-8')):
            Title.objects.bulk_create([
                Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category'],
                )
            ])

        for row in DictReader(open(FILE_PATH + MODELS[GenreTitle],
                              encoding='utf-8')):
            GenreTitle.objects.bulk_create([
                GenreTitle(
                    id=row['id'],
                    title_id=row['title_id'],
                    genre_id=row['genre_id'],
                )
            ])

        for row in DictReader(open(FILE_PATH + MODELS[User],
                              encoding='utf-8')):
            User.objects.bulk_create([
                User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )
            ])

        for row in DictReader(open(FILE_PATH + MODELS[Review],
                              encoding='utf-8')):
            Review.objects.bulk_create([
                Review(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
            ])

        for row in DictReader(open(FILE_PATH + MODELS[Comments],
                              encoding='utf-8')):
            Comments.objects.bulk_create([
                Comments(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date'],
                )
            ])

        return self.stdout.write(self.style.SUCCESS(DONE_MESSAGE))
