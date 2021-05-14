import sqlite3
import argparse

from os import getenv
from dotenv import load_dotenv
load_dotenv()

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from postgres_saver import PostgresSaver
from sqliteloader import sqliteloader


def parse_args():
    parser = argparse.ArgumentParser(description='Migrate movies from Sqlite to Postgresql in chunks')
    parser.add_argument('--start', type=int, default=0, help='Starting movie index (default=0)')
    parser.add_argument('--limit', type=int, default=1000, help='Number of movies to migrate (default=1000)')
    parser.add_argument('--reset', action='store_true', help='Empty target tables before migrating')
    return parser.parse_args()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""

    postgres_saver = PostgresSaver(pg_conn)

    args = parse_args()
    if args.reset:
        postgres_saver.reset()

    movies_iterator = sqliteloader(connection, args.start, args.limit)
    migrated = postgres_saver.save_all_data(movies_iterator)
    print("\n%d movies were migrated" % migrated)


if __name__ == '__main__':
    dsl = {'dbname': getenv('DB_NAME', 'movies'),
           'user': getenv('DB_USER', 'movies'),
           'password': getenv('DB_PASSWORD', 'movies'),
           'host': getenv('DB_HOST', '127.0.0.1'),
           'port': getenv('DB_PORT', '5432'),
           }

    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
