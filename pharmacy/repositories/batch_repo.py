from database.connection import get_connection
from models.batch import Batch


class BatchRepository:

    def add(
        self,
        medicine_id: int,
        supplier_id: int,
        batch_number: str,
        manufacture_date: str,
        expiration_date: str,
        quantity: int,
        purchase_price: float
    ) -> int:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO batches(
                medicine_id, supplier_id, batch_number,
                manufacture_date, expiration_date,
                quantity, purchase_price
            ) VALUES(?, ?, ?, ?, ?, ?, ?)
        """, (
            int(medicine_id),
            int(supplier_id),
            batch_number.strip(),
            manufacture_date.strip(),
            expiration_date.strip(),
            int(quantity),
            float(purchase_price)
        ))

        conn.commit()
        batch_id = cur.lastrowid
        conn.close()
        return batch_id


    def list_all(self) -> list[Batch]:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                b.id,
                b.medicine_id,
                b.supplier_id,
                b.batch_number,
                b.manufacture_date,
                b.expiration_date,
                b.quantity,
                b.purchase_price,
                b.created_at,
                m.name,
                s.name
            FROM batches b
            JOIN medicines m ON m.id = b.medicine_id
            JOIN suppliers s ON s.id = b.supplier_id
            ORDER BY b.expiration_date ASC, b.id ASC
        """)

        rows = cur.fetchall()
        conn.close()

        return [
            Batch(
                id=r[0],
                medicine_id=r[1],
                supplier_id=r[2],
                batch_number=r[3],
                manufacture_date=r[4],
                expiration_date=r[5],
                quantity=r[6],
                purchase_price=r[7],
                created_at=r[8],
                medicine_name=r[9],
                supplier_name=r[10],
            )
            for r in rows
        ]


    def decrease_quantity(self, batch_id: int, qty: int):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE batches
            SET quantity = quantity - ?
            WHERE id = ?
        """, (int(qty), int(batch_id)))

        conn.commit()
        conn.close()


    # ---------------------------------
    # 🔹 отримати партії препарату
    # ---------------------------------

    def get_batches_by_medicine(self, medicine_id: int):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                batch_number,
                expiration_date,
                quantity,
                purchase_price
            FROM batches
            WHERE medicine_id = ?
              AND quantity > 0
            ORDER BY expiration_date ASC
        """, (int(medicine_id),))

        rows = cur.fetchall()
        conn.close()

        return rows

    # ---------------------------------
    # отримати одну партію
    # ---------------------------------

    def get_batch(self, batch_id: int):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                medicine_id,
                supplier_id,
                batch_number,
                manufacture_date,
                expiration_date,
                quantity,
                purchase_price
            FROM batches
            WHERE id = ?
        """, (int(batch_id),))

        row = cur.fetchone()
        conn.close()

        return row