import mysql.connector


def _connect(user, host, port, database):
    return mysql.connector.connect(user=user, host=host, port=port, database=database)


class DoltConnection(object):
    def __init__(self, user='root', host='127.0.0.1', port=3306, database='dolt', auto_commit=False):
        self.user = user
        self.host = host
        self.port = port
        self.database = database
        self.auto_commit = auto_commit
        self.cnx = None

    def connect(self):
        self.cnx = _connect(self.user, self.host, self.port, self.database)
        self.cnx.autocommit = self.auto_commit

    def close(self):
        self.cnx.close()

    def query(self, query_str):
        cursor = self.cnx.cursor()
        cursor.execute(query_str)

        if cursor.description is None:
            return [], cursor.rowcount

        raw = cursor.fetchall()

        row_maps = []
        for curr in raw:
            r = {}
            for i, k in enumerate(cursor.column_names):
                r[k] = str(curr[i])
            row_maps.append(r)

        return row_maps, cursor.rowcount

