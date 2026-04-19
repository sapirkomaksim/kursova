import unittest
import sqlite3

from database.schema import SCHEMA_SQL
from repositories.batch_repo import BatchRepository
from repositories.medicine_repo import MedicineRepository
from repositories.supplier_repo import SupplierRepository


class TestBatchRepository(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        cur = self.conn.cursor()
        cur.executescript(SCHEMA_SQL)
        self.conn.commit()

        self.med_repo = MedicineRepository(conn=self.conn)
        self.sup_repo = SupplierRepository(conn=self.conn)
        self.batch_repo = BatchRepository(conn=self.conn)

    def tearDown(self):
        self.conn.close()

    def test_negative_quantity(self):

        med_id = self.med_repo.add("Med", "M", None, 0, 10)
        sup_id = self.sup_repo.add("Sup", None, None, None, None)

        with self.assertRaises(Exception):
            self.batch_repo.add(
                med_id,
                sup_id,
                "B1",
                "2024",
                "2025",
                -5,
                10
            )