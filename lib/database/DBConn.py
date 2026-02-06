import setting_for_sda.config as conf
import psycopg2
import psycopg2.extras

class DBConn:
    _instance = None
    _conn = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBConn, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._conn is None:
            self._conn = psycopg2.connect(
                            host    =conf.database_info['host'],
                            dbname  =conf.database_info['dbname'],
                            user    =conf.database_info['user'],
                            password=conf.database_info['password']
                        )
            with self._conn.cursor() as cur:
                cur.execute(f"SET search_path TO {conf.database_info['schema']}")

    def cursor(self):
        """항상 새로운 cursor 반환"""
        return self._conn.cursor()

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()

