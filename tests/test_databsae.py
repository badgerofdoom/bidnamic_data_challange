import unittest
from src.database import Database


class TestDdatabase(unittest.TestCase):

    def setUp(self) -> None:
        self.db = Database('Test_db', 'localhost', 5432)
        self.username = 'tester'
        self.password = 'tester'

    def test_a_database_instance_can_be_created(self):
        self.assertIsInstance(self.db, Database)

    def test_connection_can_be_made_to_db(self):
        result = self.db.connect(
            db_user=self.username, db_password=self.password)
        self.assertTrue(result)

    def test_incorrect_username_fails_db_connection(self):
        result = self.db.connect(
            db_user='fail', db_password=self.password)
        self.assertFalse(result)

    def test_incorrect_password_fails_db_connection(self):
        result = self.db.connect(
            db_user=self.username, db_password='fail')
        self.assertFalse(result)

    def test_incorrect_username_and_password_fails_db_connection(self):
        result = self.db.connect(
            db_user='fail', db_password='fail')
        self.assertFalse(result)

    def test_able_to_run_code_against_connection(self):
        self.db.connect(
            db_user=self.username, db_password=self.password)
        sql = 'SELECT 1 AS col_one'
        conn = self.db.connection
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        self.assertEqual(1, result[0][0])

    def test_correct_connection_string_is_created(self):
        self.db.connect(
            db_user=self.username, db_password=self.password)
        result = self.db.get_connection_string(
            db_user=self.username, db_password=self.password)
        expected = 'postgresql://tester:tester@localhost:5432/Test_db'
        self.assertEqual(
            result, expected)
