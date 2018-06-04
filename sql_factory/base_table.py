import typing

from sqlalchemy import *


class BaseTable():
    _engine = None
    _cur_table_name = None
    connect = None
    table_cmd = None

    is_base_table = False

    def __init__(self, db_connect: create_engine, table_name=None, is_base_table=False):
        self._engine = db_connect
        self._cur_table_name = table_name if table_name is not None else self.__class__.__name__
        self._cur_table_name = self._cur_table_name.lower()
        self.is_base_table = is_base_table
        self.create_table()
        if self.connect is None:  # pragma: no cover
            raise BaseException("you must assign table connection to self.connect")

    def create_table(self):
        metadata = MetaData(self._engine)
        self.connect = Table(self._cur_table_name, metadata, autoload=True)

    def update(self, condition, update_content):
        stmt = self.connect.update().values(update_content)
        for k in condition:
            stmt = stmt.where(getattr(self.connect.c, k) == condition[k])
        self._engine.execute(stmt)

    def insert(self, document: dict):
        if document == {}:
            return
        self._engine.execute(self.connect.insert(), document)

    def remove(self, condition: dict = None):
        if condition is None:
            d = self.connect.delete()
        else:
            d = self.connect.delete()
            for k in condition:
                d = d.where(getattr(self.connect.c, k) == condition[k])
        self._engine.execute(d)

    def get(self, condition=None) -> typing.List[dict]:
        if condition is None:
            s = select([self.connect])
        else:
            s = select([self.connect])
            for k in condition:
                s = s.where(getattr(self.connect.c, k) == condition[k])
        res = self._engine.execute(s).fetchall()
        return self.sql_res_to_list_dict(res)

    def count(self) -> int:
        return self._engine.execute(select([func.count()]).select_from(self.connect)).fetchone()[0]

    def get_all(self) -> typing.List[dict]:
        return self.get()

    def get_connect(self):
        return self.connect

    def get_engine(self):
        return self._engine

    def sql_res_to_list_dict(self, res, col_name_list=None):
        if col_name_list is None:
            col_name_list = self.connect.columns.keys()
        if not isinstance(col_name_list, list):  # pragma: no cover
            col_name_list = [col_name_list]
        if res:
            record_list = []
            for e in res:
                d = dict(zip(col_name_list, e))
                record_list.append(d)
            return record_list
        else:
            return []
