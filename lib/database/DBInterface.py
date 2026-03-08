import lib.database.DBConn as db_conn

class DBInterface:
    def __init__(self):
        self.db_conn = db_conn.DBConn()

    def execute_query(self, query, params=None):
        with self.db_conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
        