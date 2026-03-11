from database.connection import get_connection
from models.customer import Customer

class CustomerRepository:

    def add(self, full_name: str, phone: str | None = None) -> int:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO customers(full_name, phone) VALUES(?, ?)",
            (full_name.strip(), phone)
        )

        conn.commit()
        cid = cur.lastrowid
        conn.close()
        return cid

    def list_all(self) -> list[Customer]:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, full_name, phone, created_at
            FROM customers
            ORDER BY full_name
        """)

        rows = cur.fetchall()
        conn.close()

        return [Customer(*row) for row in rows]

    def update(self, customer_id: int, full_name: str, phone: str | None) -> None:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE customers
            SET full_name=?, phone=?
            WHERE id=?
        """, (full_name.strip(), phone, int(customer_id)))

        conn.commit()
        conn.close()

    def delete(self, customer_id: int) -> None:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM customers WHERE id=?", (int(customer_id),))

        conn.commit()
        conn.close()