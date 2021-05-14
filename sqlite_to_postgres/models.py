from dataclasses import dataclass, field, fields
import uuid
from typing import ClassVar
from psycopg2._psycopg import cursor as _cursor
import psycopg2.extras
from dataclasses import astuple

psycopg2.extras.register_uuid()


class Model:
    """Base class for models"""

    # database table name
    _table: ClassVar[str]

    # field that determine uniqueness of the record
    _uniq_field: ClassVar[str]

    def save(self, cursor: _cursor):
        data = astuple(self)
        names = ",".join(['"%s"' % f.name for f in fields(self)])

        template = ",".join(["%s"] * len(data))
        values = cursor.mogrify(template, data).decode()
        sql = f"""
            insert into {self._table} ({names}) values ({values}) on conflict do nothing
              """

        if hasattr(self, 'id'):
            sql += " returning *"

        cursor.execute(sql)

        # If the entry is found, correct the auto-generated object.id with the value from database.
        if hasattr(self, 'id'):
            result = cursor.fetchone()
            # nothing was inserted
            if not result:
                sql = f"select id from {self._table} where {self._uniq_field}=%s"
                cursor.execute(sql, (getattr(self, self._uniq_field),))
                result2 = cursor.fetchone()
                self.id = result2[0]



@dataclass
class FilmWork(Model):
    title: str
    description: str
    rating: float
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    _table: ClassVar[str] = "film_work"
    _uniq_field: ClassVar[str] = "title"


@dataclass
class Genre(Model):
    name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    _table: ClassVar[str] = "genre"
    _uniq_field: ClassVar[str] = "name"


@dataclass
class Person(Model):
    full_name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    _table: ClassVar[str] = "person"
    _uniq_field: ClassVar[str] = "full_name"


@dataclass
class FilmWorkGenre(Model):
    film_work_id_id: uuid.UUID
    genre_id_id: uuid.UUID
    _table: ClassVar[str] = "film_work_genre"


@dataclass
class FilmWorkPerson(Model):
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    _table: ClassVar[str] = "film_work_person"
