from sql_factory.base_table import BaseTable
from sqlalchemy import MetaData, Table, Column, String, select, Integer


class ExaTable(BaseTable):
    def create_table(self):
        try:
            metadata = MetaData()
            table_connect = Table('exa_table', metadata,
                                  Column('id', Integer, primary_key=True),
                                  Column('name', String(50)),
                                  )
            metadata.create_all(self.engine)
            self.connect = table_connect
        except BaseException as e:  # pragma: no cover
            print("Create table 'table' failed: " + e.__str__())
            return False

    def insert_by_id(self, id: int, content: dict):
        if "id" not in content.keys():
            content["id"] = id
        self.insert(content)
