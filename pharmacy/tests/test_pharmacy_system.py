import unittest
import sqlite3

from repositories.medicine_repo import MedicineRepository
from repositories.batch_repo import BatchRepository
from repositories.sale_repo import SaleRepository


# -----------------------------
# Ініціалізація тестової БД
# -----------------------------
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


# =============================
# ТЕСТИ
# =============================
class TestPharmacySystem(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        init_db(self.conn)

        self.medicine_repo = MedicineRepository(conn=self.conn)
        self.batch_repo = BatchRepository(conn=self.conn)
        self.sale_repo = SaleRepository(conn=self.conn)

    # -------------------------
    # Створення препарату
    # -------------------------
    def test_create_medicine(self):
        med_id = self.medicine_repo.add(
            "Test medicine", "Test", None, False, 10.0
        )
        self.assertIsNotNone(med_id)

    # -------------------------
    # Список препаратів
    # -------------------------
    def test_list_medicines(self):
        self.medicine_repo.add("A", None, None, False, 10.0)
        self.medicine_repo.add("B", None, None, False, 20.0)

        medicines = self.medicine_repo.list_all()
        self.assertEqual(len(medicines), 2)

    # -------------------------
    # Створення партії
    # -------------------------
    def test_create_batch(self):
        med_id = self.medicine_repo.add("Test", None, None, False, 10.0)

        batch_id = self.batch_repo.add(
            med_id, 1, "B1",
            "2024-01-01", "2026-01-01",
            100, 5.0
        )

        self.assertIsNotNone(batch_id)

    # -------------------------
    # Зменшення кількості
    # -------------------------
    def test_decrease_quantity(self):
        med_id = self.medicine_repo.add("Test", None, None, False, 10.0)

        batch_id = self.batch_repo.add(
            med_id, 1, "B1",
            "2024-01-01", "2026-01-01",
            20, 5.0
        )

        self.batch_repo.decrease_quantity(batch_id, 5)
        batch = self.batch_repo.get_batch(batch_id)

        self.assertEqual(batch[6], 15)

    # -------------------------
    # Не можна списати більше ніж є
    # -------------------------
    def test_cannot_decrease_below_zero(self):
        med_id = self.medicine_repo.add("Test", None, None, False, 10.0)

        batch_id = self.batch_repo.add(
            med_id, 1, "B1",
            "2024-01-01", "2026-01-01",
            5, 5.0
        )

        with self.assertRaises(Exception):
            self.batch_repo.decrease_quantity(batch_id, 10)

    # -------------------------
    # Продаж
    # -------------------------
    def test_sale_and_quantity_decrease(self):
        med_id = self.medicine_repo.add("Test", None, None, False, 10.0)

        batch_id = self.batch_repo.add(
            med_id, 1, "B1",
            "2024-01-01", "2026-01-01",
            50, 5.0
        )

        sale_id = self.sale_repo.create_sale(1, 1)

        self.sale_repo.add_item(sale_id, batch_id, 10, 10.0)
        self.batch_repo.decrease_quantity(batch_id, 10)

        batch = self.batch_repo.get_batch(batch_id)
        self.assertEqual(batch[6], 40)

    # -------------------------
    # Total сума
    # -------------------------
    def test_sale_total(self):
        med_id = self.medicine_repo.add("Test", None, None, False, 10.0)

        batch_id = self.batch_repo.add(
            med_id, 1, "B1",
            "2024-01-01", "2026-01-01",
            50, 5.0
        )

        sale_id = self.sale_repo.create_sale(1, 1)

        self.sale_repo.add_item(sale_id, batch_id, 2, 10.0)
        self.sale_repo.update_total(sale_id)

        cur = self.conn.cursor()
        cur.execute("SELECT total_amount FROM sales WHERE id=?", (sale_id,))
        total = cur.fetchone()[0]

        self.assertEqual(total, 20.0)

    # -------------------------
    # Від’ємна ціна
    # -------------------------
    def test_negative_price(self):
        with self.assertRaises(ValueError):
            self.medicine_repo.add("Bad", None, None, False, -5.0)

    # -------------------------
    # Видалення
    # -------------------------
    def test_delete_medicine(self):
        med_id = self.medicine_repo.add("Test", None, None, False, 10.0)
        self.medicine_repo.delete(med_id)

        medicines = self.medicine_repo.list_all()
        self.assertEqual(len(medicines), 0)

    # -------------------------
    # Отримання batch
    # -------------------------
    def test_get_batch(self):
        med_id = self.medicine_repo.add("Test", None, None, False, 10.0)

        batch_id = self.batch_repo.add(
            med_id, 1, "B1",
            "2024-01-01", "2026-01-01",
            10, 5.0
        )

        batch = self.batch_repo.get_batch(batch_id)

        self.assertIsNotNone(batch)
        self.assertEqual(batch[0], batch_id)

    def tearDown(self):
        self.conn.close()


if __name__ == "__main__":
    unittest.main()