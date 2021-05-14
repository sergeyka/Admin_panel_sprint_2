import json
from json import JSONDecodeError


class sqliteloader:
    """Extract from SQLite and transform movies, correcting their structure"""
    def __init__(self, conn, start: int, limit: int):

        self.conn = conn

        def dict_factory(cursor, row):
            _ = {}
            for idx, col in enumerate(cursor.description):
                _[col[0]] = row[idx]
            return _

        conn.row_factory = dict_factory

        self.start = start
        self.limit = limit

    def __iter__(self):
        sql = "select * from movies m order by id limit ? offset ?"
        self.cursor = self.conn.cursor()

        for row in self.cursor.execute(sql, (self.limit, self.start)):
            doc = {
                'id': row['id'],
                'imdb_rating': self.float_or_none(row['imdb_rating']),
                'genre': [_.strip() for _ in row['genre'].split(',')],
                'title': row['title'],
                'director': [] if row['director'] == 'N/A' else [_.strip() for _ in row['director'].split(',')],
                'description': None if row['plot'] == 'N/A' else row['plot'],
            }

            writer_ids = set()
            if row['writer']:
                writer_ids.add(row['writer'])
            elif row['writers']:
                try:
                    writers = json.loads(row['writers'])
                    for writer in writers:
                        writer_ids.add(writer['id'])
                except JSONDecodeError:
                    print("unable to parse " + row['writers'])

            doc['writer'] = self.get_writers_by_ids(writer_ids)
            doc['actor'] = self.get_actors_by_movie_id(doc['id'])

            yield doc

    @staticmethod
    def float_or_none(value):
        try:
            return float(value)
        except ValueError:
            return None

    def get_writers_by_ids(self, ids):
        placeholders = ",".join(["?"] * len(ids))
        query = f"select id, name from writers where id in({placeholders}) and name <> 'N/A'"
        result = set()
        for w in self.conn.cursor().execute(query, list(ids)):
            if not w['name']:
                continue
            result.add(w['name'])

        return result

    def get_actors_by_movie_id(self, movie_id):
        query = """select a.id, a.name 
                   from actors a 
                   join movie_actors ma on a.id=ma.actor_id 
                   join movies m on ma.movie_id=m.id where m.id=?"""
        result = set()
        for a in self.conn.cursor().execute(query, (movie_id,)):
            if not a['name'] or a['name'] == 'N/A':
                continue
            result.add(a['name'])

        return result
