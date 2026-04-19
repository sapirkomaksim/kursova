import unittest
import sqlite3

from repositories.medicine_repo import MedicineRepository
from repositories.batch_repo import BatchRepository
from repositories.sale_repo import SaleRepository


def init_db(conn):
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    );

    CREATE TABLE medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        manufacturer TEXT,
        category_id INTEGER,
        prescription_required INTEGER,
        retail_price REAL
    );

    CREATE TABLE batches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_id INTEGER,
        supplier_id INTEGER,
        batch_number TEXT,
        manufacture_date TEXT,
        expiration_date TEXT,
        quantity INTEGER,
        purchase_price REAL
    );

    CREATE TABLE sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        customer_id INTEGER,
        total_amount REAL DEFAULT 0
    );

    CREATE TABLE sale_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER,
        batch_id INTEGER,
        quantity INTEGER,
        price REAL
    );
    """)

    conn.commit()


class TestExtraPharmacySystem(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        init_db(self.conn)

        self.medicine_repo = MedicineRepository(conn=self.conn)
        self.batch_repo = BatchRepository(conn=self.conn)
        self.sale_repo = SaleRepository(conn=self.conn)

    # 1. Не можна створити партію з від’ємною кількістю
    def test_add_batch_negative_quantity(self):
        med_id = self.medicine_repo.add("Paracetamol", "Test", None, False, 20.0)

        with self.assertRaises(ValueError):
            self.batch_repo.add(
                med_id, 1, "B-001",
                "2024-01-01", "2026-01-01",
                -10, 5.0
            )

    # 2. Не можна створити партію з від’ємною закупівельною ціною
    def test_add_batch_negative_purchase_price(self):
        med_id = self.medicine_repo.add("Ibuprofen", "Test", None, False, 30.0)

        with self.assertRaises(ValueError):
            self.batch_repo.add(
                med_id, 1, "B-002",
                "2024-01-01", "2026-01-01",
                10, -3.0
            )

    # 3. Не можна списувати 0 одиниць
    def test_decrease_quantity_zero_raises(self):
        med_id = self.medicine_repo.add("Aspirin", "Test", None, False, 15.0)

        batch_id = self.batch_repo.add(
            med_id, 1, "B-003",
            "2024-01-01", "2026-01-01",
            20, 4.0
        )

        with self.assertRaises(ValueError):
            self.batch_repo.decrease_quantity(batch_id, 0)

    # 4. Метод get_batches_by_medicine повертає лише партії з quantity > 0
    #    і впорядковує їх за датою придатності
    def test_get_batches_by_medicine_sorted_and_positive_only(self):
        med_id = self.medicine_repo.add("Nurofen", "Test", None, False, 25.0)

        self.batch_repo.add(
            med_id, 1, "B-early",
            "2024-01-01", "2025-06-01",
            5, 6.0
        )

        self.batch_repo.add(
            med_id, 1, "B-zero",
            "2024-01-01", "2025-01-01",
            0, 6.0
        )

        self.batch_repo.add(
            med_id, 1, "B-late",
            "2024-01-01", "2025-12-01",
            7, 6.0
        )

        batches = self.batch_repo.get_batches_by_medicine(med_id)

        self.assertEqual(len(batches), 2)
        self.assertEqual(batches[0][1], "B-early")
        self.assertEqual(batches[1][1], "B-late")

    # 5. Загальна сума продажу правильно рахується для кількох позицій
    def test_sale_total_multiple_items(self):
        med1_id = self.medicine_repo.add("Medicine A", "Test", None, False, 10.0)
        med2_id = self.medicine_repo.add("Medicine B", "Test", None, False, 20.0)

        batch1_id = self.batch_repo.add(
            med1_id, 1, "B-A",
            "2024-01-01", "2026-01-01",
            50, 5.0
        )

        batch2_id = self.batch_repo.add(
            med2_id, 1, "B-B",
            "2024-01-01", "2026-01-01",
            50, 8.0
        )

        sale_id = self.sale_repo.create_sale(1, 1)

        self.sale_repo.add_item(sale_id, batch1_id, 2, 10.0)   # 20
        self.sale_repo.add_item(sale_id, batch2_id, 3, 20.0)   # 60
        self.sale_repo.update_total(sale_id)

        cur = self.conn.cursor()
        cur.execute("SELECT total_amount FROM sales WHERE id=?", (sale_id,))
        total = cur.fetchone()[0]

        self.assertEqual(total, 80.0)

    def tearDown(self):
        self.conn.close()


if __name__ == "__main__":
    unittest.main()