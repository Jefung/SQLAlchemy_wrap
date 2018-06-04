import unittest
from sql_factory import MysqlFactory
from exceptions import DbNotConnect


class TestIProject(unittest.TestCase):
    db_name = "unittest"
    username = "root"
    password = "jefung"

    def test_operator_table_class(self):
        db_factory = MysqlFactory("tests.table_class")
        db_factory.db(self.db_name, self.username, self.password)
        table_class = db_factory.db(self.db_name).table("unittest_table")

        table_class.remove({"id": 1})
        count = table_class.count()
        table_class.insert_by_id(1, {"name": "unittest"})
        self.assertEqual(count + 1, table_class.count())
        table_class.remove()

    def test_db_exception(self):
        db_factory = MysqlFactory()
        self.assertRaises(DbNotConnect, db_factory.db, self.db_name)

    def test_db_conect(self):

        db_factory = MysqlFactory()
        self.assertRaises(DbNotConnect, db_factory.db, self.db_name)

        sql_url = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(self.username,self.password,"localhost",self.db_name)
        db_factory.connect(self.db_name,sql_url)
        self.assertIsInstance(db_factory.db(self.db_name),MysqlFactory)

        # close db connection
        db_factory.db(self.db_name).close()
        self.assertRaises(DbNotConnect, db_factory.db, self.db_name)

        self.assertIsInstance(db_factory.db(self.db_name,self.username,self.password), MysqlFactory)


    def test_base_table_class(self):
        db_factory = MysqlFactory("not_this_path")
        # db_factory.db_connect(self.db_name, self.username, self.password)
        t = db_factory.db(self.db_name, self.username, self.password)
        t = db_factory.db(self.db_name).table("unittest_table")

        # test count
        self.assertIsInstance(t.count(), int)

        # test insert and remove
        t.remove()
        count = t.count()
        t.insert({"id": 1, "name": "unittest"})
        self.assertEqual(count + 1, t.count())
        t.remove()
        self.assertEqual(0, t.count())

        # test get and get_all
        t.insert({"id": 1, "name": "unittest"})
        self.assertIsInstance(t.get({"id": 1}), list)
        self.assertEqual(t.get({"id": 1})[0]["name"], "unittest")

        t.insert({"id": 2, "name": "unittest"})
        self.assertEqual(2, len(t.get_all()))
        t.remove()

        # test update
        t.insert({"id": 1, "name": "unittest"})
        self.assertEqual(t.get({"id": 1})[0]["name"], "unittest")
        t.update({"id": 1}, {"name": "update"})
        self.assertEqual(t.get({"id": 1})[0]["name"], "update")
        t.remove()


if __name__ == '__main__':
    unittest.main()
