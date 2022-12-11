from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    """
    Проверяет, чтобы год выпуска не был больше текущего.
    """
    if value > datetime.now().year:
        raise ValidationError(
            'Год выпуска произведения не может быть больше текущего.',
            params={'value': value},
        )
