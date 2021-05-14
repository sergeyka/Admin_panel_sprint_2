import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FilmWorkType(models.TextChoices):
    MOVIE = 'movie', _('фильм')
    TV_SHOW = 'tv_show', _('шоу')


class RoleType(models.TextChoices):
    WRITER = 'writer', _('сценарист')
    DIRECTOR = 'director', _('режиссер')
    ACTOR = 'actor', _('актер')


class Genre(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(_('название'), max_length=255, unique=True)
    description = models.TextField(_('описание'), blank=True)

    class Meta:
        db_table = 'genre'
        verbose_name = _('жанр')
        verbose_name_plural = _('жанры')

    def __str__(self):
        return self.name


class FilmWork(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(_('название'), max_length=255, unique=True)
    description = models.TextField(_('описание'), blank=True, null=True)
    certificate = models.TextField(_('сертификат'), blank=True)
    file_path = models.FileField(_('файл'), upload_to='film_works/', blank=True)
    rating = models.FloatField(_('рейтинг'), validators=[MinValueValidator(0)], blank=True)
    type = models.CharField(_('тип'), max_length=20, choices=FilmWorkType.choices)
    creation_date = models.DateField(_('дата выхода'), blank=True, null=True)

    class Meta:
        db_table = 'film_work'
        verbose_name = _('кинопроизведение')
        verbose_name_plural = _('кинопроизведения')

    def __str__(self):
        return self.title


class FilmWorkGenre(models.Model):
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE, related_name='film_genres')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='film_works')

    class Meta:
        db_table = 'film_work_genre'
        unique_together = (('film_work_id', 'genre_id'),)


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    full_name = models.CharField(_('полное имя'), max_length=255, unique=True)

    class Meta:
        db_table = 'person'
        verbose_name = _('персона')
        verbose_name_plural = _('персоны')

    def __str__(self):
        return self.full_name


class FilmWorkPerson(TimeStampedModel):
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE, verbose_name=_('фильм'),
                                  related_name='persons')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name=_('персона'),
                               related_name='film_works')
    role = models.CharField(_('профессия'), choices=RoleType.choices, max_length=255)

    class Meta:
        db_table = 'film_work_person'
        verbose_name = _('персона')
        verbose_name_plural = _('персоны')
        unique_together = (('film_work', 'person', 'role'),)
