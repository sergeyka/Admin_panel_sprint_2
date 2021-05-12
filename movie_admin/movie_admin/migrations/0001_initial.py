# Generated by Django 3.1 on 2021-04-24 17:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FilmWork',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='описание')),
                ('creation_date', models.DateField(blank=True, verbose_name='дата создания фильма')),
                ('certificate', models.TextField(blank=True, verbose_name='сертификат')),
                ('file_path', models.FileField(blank=True, upload_to='film_works/', verbose_name='файл')),
                ('rating', models.FloatField(blank=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='рейтинг')),
                ('type', models.CharField(choices=[('movie', 'фильм'), ('tv_show', 'шоу')], max_length=20, verbose_name='тип')),
            ],
            options={
                'verbose_name': 'кинопроизведение',
                'verbose_name_plural': 'кинопроизведения',
                'db_table': 'film_work',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
            ],
            options={
                'verbose_name': 'жанр',
                'verbose_name_plural': 'жанры',
                'db_table': 'genre',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255, verbose_name='полное имя')),
                ('birth_date', models.DateField(verbose_name='дата рождения')),
            ],
            options={
                'verbose_name': 'персона',
                'verbose_name_plural': 'персоны',
                'db_table': 'person',
            },
        ),
        migrations.CreateModel(
            name='FilmWorkPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('role', models.CharField(max_length=255, verbose_name='профессия')),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persons', to='movie_admin.filmwork', verbose_name='фильм')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='film_works', to='movie_admin.person', verbose_name='персона')),
            ],
            options={
                'verbose_name': 'персона',
                'verbose_name_plural': 'персоны',
                'db_table': 'film_work_person',
                'unique_together': {('film_work', 'person', 'role')},
            },
        ),
        migrations.CreateModel(
            name='FilmWorkGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('film_work_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genres', to='movie_admin.filmwork')),
                ('genre_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='film_works', to='movie_admin.genre')),
            ],
            options={
                'db_table': 'film_work_genre',
                'unique_together': {('film_work_id', 'genre_id')},
            },
        ),
    ]