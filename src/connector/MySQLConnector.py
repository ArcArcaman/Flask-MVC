import mysql.connector as sql

host = 'localhost'
user = 'user'
password = 'password'

class MySQL:
    def __init__(self, dbname):
        self.__mydb = sql.connect(
            host=host,
            user=user,
            password=password
        )
        self.__cur = self.__mydb.cursor()
        self.__cur.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s",[dbname])
        if len(self.__cur.fetchall()) == 0: assert "Database {} not found".format(dbname)
        self.__mydb.close()
        self.__mydb = sql.connect(
            host=host,
            user=user,
            password=password,
            database=dbname
        )
        self.__cur = self.__mydb.cursor()

    def execute(self, sql, val=None):
        if val == None: self.__cur.execute(sql)
        else: self.__cur.execute(sql, val)
        return self.__cur

    def executemany(self, sql, val_list):
        self.__cur.executemany(sql, val_list)

    def commit(self):
        self.__mydb.commit()

    def fetchall(self):
        return self.__cur.fetchall()

    def fetchone(self):
        return self.__cur.fetchone()

    def fetchmany(self):
        return self.__cur.fetchmany()