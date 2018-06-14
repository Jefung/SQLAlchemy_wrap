from sqlalchemy import Column, String, Integer

from sql_factory.base_table import BaseTable


class UnittestTable(BaseTable):
    # def create_table(self):
    #     try:
    #         metadata = MetaData()
    #         table_connect = Table('unittest_table', metadata,
    #                               Column('id', Integer, primary_key=True),
    #                               Column('name', String(50)),
    #                               )
    #         metadata.create_all(self.engine)
    #         self.connect = table_connect
    #     except BaseException as e:  # pragma: no cover
    #         print("Create table 'table' failed: " + e.__str__())
    #         return False
    table_columns = [
        Column('id', Integer, primary_key=True),
        Column('name', String(50)),
    ]

    def insert_by_id(self, id: int, content: dict):
        if "id" not in content.keys():
            content["id"] = id
        self.insert(content)
