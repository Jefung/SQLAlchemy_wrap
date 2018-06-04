import os
import unittest
import tempfile

from exceptions import *
from interfaces import IProject
from sql_factory import SqlalchemyFactory, MysqlFactory, SqliteFactory


class TestSqliteFactory(unittest.TestCase):
    temp_dir = tempfile.gettempdir()
    db_name = "py_unittest_db_name"
    db_temp_file = os.path.join(temp_dir, db_name)

    def test_connect_db(self):
        db_factory = SqliteFactory()
        self.assertRaises(DbNotConnect, db_factory.db, self.db_name)

        db_factory.db(self.db_name, self.db_temp_file)
        db_factory.db(self.db_name).close()

        self.assertRaises(DbNotConnect, db_factory.db, self.db_name)

        db_factory.connect(self.db_name, "sqlite:///" + self.db_temp_file)
        db_factory.db(self.db_name)

        if os.path.isfile(self.db_temp_file):
            os.remove(self.db_temp_file)


if __name__ == '__main__':
    unittest.main()
