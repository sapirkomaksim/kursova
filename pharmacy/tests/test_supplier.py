import unittest
import sqlite3

from database.schema import SCHEMA_SQL
from repositories.supplier_repo import SupplierRepository


class TestSupplierRepository(unittest.TestCase):

    def setUp(self):
        # створюємо тестову БД
        self.conn = sqlite3.connect(":memory:")
        cur = self.conn.cursor()
        cur.executescript(SCHEMA_SQL)
        self.conn.commit()

        self.repo = SupplierRepository(conn=self.conn)

    def tearDown(self):
        self.conn.close()

    def test_add_supplier(self):
        self.repo.add("Test Supplier", "123", "Addr", "UA", "Dist")

        suppliers = self.repo.list_all()

        self.assertEqual(len(suppliers), 1)
        self.assertEqual(suppliers[0].name, "Test Supplier")