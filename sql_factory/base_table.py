import typing

from sqlalchemy import *


class BaseTable():
    engine = None
    table_cmd = None
    connect = None
    table_columns = None
    _cur_table_name = None

    is_base_table = False

    def __init__(self, engine: create_engine, table_name=None, is_base_table=True):
        self.engine = engine
        self._cur_table_name = table_name if table_name is not None else self.__class__.__name__
        self._cur_table_name = self._cur_table_name.lower()
        self.is_base_table = is_base_table

        if self.table_columns is not None and self.connect is None:
            self.create_table_using_columns(*self.table_columns)

        if self.connect is None:
            self.create_table()

        if self.connect is None:  # pragma: no cover
            raise BaseException("you must assign table connection to self.connect")

    def create_table_using_columns(self, *args):
        try:
            metadata = MetaData()
            table_connect = Table('project', metadata, *args)
            metadata.create_all(self.engine)
            self.connect = table_connect
        except BaseException as e:  # pragma: no cover
            print("Create table 'project' using columns failed: " + e.__str__())
            return False

    def create_table(self):
        metadata = MetaData(self.engine)
        self.connect = Table(self._cur_table_name, metadata, autoload=True)

    def update(self, condition, update_content):
        stmt = self.connect.update().values(update_content)
        for k in condition:
            stmt = stmt.where(getattr(self.connect.c, k) == condition[k])
        self.engine.execute(stmt)

    def insert(self, document: dict):
        if document == {}:
            return
        self.engine.execute(self.connect.insert(), document)

    def remove(self, condition: dict = None):
        '''
            remove records that mach condition
        :param condition: if it's None, remove all record
        :return: None
        '''
        if condition is None:
            d = self.connect.delete()
        else:
            d = self.connect.delete()
            for k in condition:
                d = d.where(getattr(self.connect.c, k) == condition[k])
        self.engine.execute(d)

    def get(self, condition=None) -> typing.List[dict]:
        if condition is None:
            s = select([self.connect])
        else:
            s = select([self.connect])
            for k in condition:
                s = s.where(getattr(self.connect.c, k) == condition[k])
        res = self.engine.execute(s).fetchall()
        return self.sql_res_to_list_dict(res)

    def count(self) -> int:
        return self.engine.execute(select([func.count()]).select_from(self.connect)).fetchone()[0]

    def get_all(self) -> typing.List[dict]:
        return self.get()

    def get_connect(self):
        return self.connect

    def get_engine(self):
        return self.engine

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

    # def __del__(self):
    #     self.table_columns.clear()
    #     self.table_columns = []
