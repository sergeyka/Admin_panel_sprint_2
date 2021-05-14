from psycopg2.extensions import connection as _connection
from models import Person, FilmWorkPerson, FilmWork, Genre, FilmWorkGenre


class PostgresSaver:
    def __init__(self, pg_conn: _connection):
        self.cursor = pg_conn.cursor()
        self._counter = 0

    def reset(self):
        """Truncates content tables"""
        truncate_sql = """truncate film_work, 
                                   film_work_genre, 
                                   film_work_person, 
                                   genre,
                                   person;"""
        self.cursor.execute(truncate_sql)

    def save_all_data(self, movies_iterator) -> int:
        """
        Iterate over movies saving them in postgres content tables
        @param movies_iterator: the movies
        @return: number of movies saved
        """
        cursor = self.cursor

        for movie in movies_iterator:
            film_work = FilmWork(title=movie['title'], description=movie['description'], rating=movie['imdb_rating'])
            film_work.save(cursor)

            for role in ['actor', 'director', 'writer']:
                for person_name in movie[role]:
                    person = Person(full_name=person_name)
                    person.save(cursor)
                    FilmWorkPerson(film_work_id=film_work.id, person_id=person.id, role=role).save(cursor)

            for genre_name in movie['genre']:
                genre = Genre(name=genre_name)
                genre.save(cursor)
                FilmWorkGenre(film_work_id_id=film_work.id, genre_id_id=genre.id).save(cursor)

            self._counter += 1
            print('.', end='', flush=True)

        return self._counter
