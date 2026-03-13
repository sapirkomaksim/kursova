from database.connection import get_connection
from models.supplier import Supplier

class SupplierRepository:

    def add(self, name: str, phone: str | None = None, address: str | None = None) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO suppliers(name, phone, address) VALUES(?, ?, ?)",
            (name.strip(), phone, address)
        )
        conn.commit()
        sid = cur.lastrowid
        conn.close()
        return sid

    def list_all(self) -> list[Supplier]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, phone, address FROM suppliers ORDER BY name")
        rows = cur.fetchall()
        conn.close()
        return [Supplier(*row) for row in rows]

    def update(self, supplier_id: int, name: str, phone: str | None, address: str | None) -> None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE suppliers SET name=?, phone=?, address=? WHERE id=?",
            (name.strip(), phone, address, int(supplier_id))
        )
        conn.commit()
        conn.close()

    def delete(self, supplier_id: int) -> None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM suppliers WHERE id=?", (int(supplier_id),))
        conn.commit()
        conn.close()