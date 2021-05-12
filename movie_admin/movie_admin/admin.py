from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import FilmWorkPerson, FilmWorkGenre, FilmWork, Genre, Person


class PersonRoleInline(admin.TabularInline):
    model = FilmWorkPerson
    extra = 0


class GenreInline(admin.TabularInline):
    model = FilmWorkGenre
    extra = 0


@admin.register(FilmWork)
class FilmWorkAdmin(ModelAdmin):
    list_display = ('title', 'type', 'rating')
    fields = (
        'title', 'type', 'description', 'certificate',
        'file_path', 'rating'
    )

    inlines = [
        PersonRoleInline,
        GenreInline
    ]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    fields = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    fields = ('full_name',)
    search_fields = ('full_name',)
