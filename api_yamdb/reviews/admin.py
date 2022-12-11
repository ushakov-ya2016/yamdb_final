from django.contrib import admin

from .models import Category, Genre, GenreTitle, Title, Review, Comments


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
    )
    list_editable = ('category', )
    search_fields = ('name', 'year', )
    list_filter = ('category', 'year', )
    empty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comments)
admin.site.register(GenreTitle)
