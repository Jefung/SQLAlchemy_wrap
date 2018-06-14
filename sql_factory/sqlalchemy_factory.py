import sqlalchemy
from sqlalchemy import create_engine

from exceptions import DbNotConnect
from interfaces import IDbFactory
from .base_table import BaseTable


class SqlalchemyFactory(IDbFactory):
    _dbs = {}
    _tables = {}
    _connect = None
    _cur_db = None
    _cur_db_name = None
    _cur_col = None
    _db_dir = None
    engine = None

    def __init__(self, db_dir: str = None):
        '''
            assign database dir that contain table operator class
        :param db_dir: if db_dir is None, table('table_name') will return BaseTable(), if it's "", it will find in
                       current dir, otherwise find in db_dir

        '''
        self._db_dir = db_dir

    def connect(self, db_name, *args, **kw):
        """
            add a database connection, it will not set the instance's current db connect
        """
        self.engine = create_engine(*args, **kw)
        self._dbs[db_name] = self.engine.connect()
        self._tables[db_name] = {}
        self._cur_db = self._dbs[db_name]
        self._cur_db_name = db_name

    def db(self, db_name):
        """
            set the current db connection for instance, if database_name is not connected, it will attempt to
            connect
        :return: IDbFactory
        """
        if db_name in self._dbs:
            self._cur_db = self._dbs[db_name]
            self._cur_db_name = db_name
            return self
        else:
            raise DbNotConnect("database '" + db_name + "' is not connect, you can use connect() to connect db")

            # attempt to connect  database
            # self.connect(database_name, *args, **kw)
            # return self

    def table(self, table_name: str):
        table_name = table_name.lower()

        if table_name not in self._tables[self._cur_db_name]:
            self._tables[self._cur_db_name][table_name] = self.get_table_operate_class(self._cur_db_name, table_name)

        self._cur_col = self._tables[self._cur_db_name][table_name]
        return self._cur_col

    def get_table_operate_class(self, db_name: str, table_name: str):
        saved_table_name = table_name
        try:
            table_name = table_name.replace("_", "")

            if self._db_dir is None:
                return BaseTable(self._cur_db, saved_table_name)
            elif self._db_dir == "":
                __import__(db_name)
            else:
                __import__(self._db_dir + "." + db_name)

            m = __import__(self._db_dir + "." + db_name, fromlist=[table_name])
            for attr_name in dir(m):
                if table_name.lower() == attr_name.lower():
                    if type(getattr(m, attr_name)) == type and \
                            issubclass(getattr(m, attr_name), BaseTable):
                        table_name = attr_name
                        break
            cls = getattr(m, table_name)
            return cls(self._cur_db, is_base_table=False)
        except Exception as e:
            base_table = BaseTable(self._cur_db, saved_table_name)
            return base_table
        except ModuleNotFoundError:
            base_table = BaseTable(self._cur_db, saved_table_name)
            return base_table

    def table_drop(self, table_name, database_name=None):
        pass

    def close(self):
        if self._cur_db:
            self._cur_db.close()
            self._dbs.pop(self._cur_db_name)
            self._tables.pop(self._cur_db_name)
            self._cur_db_name = None
            self._cur_col = None

    def exec(self, *args, **kw) -> sqlalchemy.engine.result.ResultProxy:
        """
           execute sql in current db connect
        """
        return self._cur_db.execute(*args, **kw)

    def get_engine(self):
        return self.engine

    def __del__(self):
        self._dbs.clear()
        self._tables.clear()
