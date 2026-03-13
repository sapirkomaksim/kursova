from database.connection import get_connection


class SaleRepository:

    # -----------------------------------
    # Створення продажу
    # -----------------------------------

    def create_sale(self, user_id: int, customer_id: int) -> int:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO sales(user_id, customer_id, total_amount)
            VALUES(?, ?, 0)
        """, (int(user_id), int(customer_id)))

        conn.commit()
        sale_id = cur.lastrowid
        conn.close()

        return sale_id

    # -----------------------------------
    # Додавання позиції
    # -----------------------------------

    def add_item(self, sale_id: int, batch_id: int, qty: int, price: float):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO sale_items(sale_id, batch_id, quantity, price)
            VALUES(?, ?, ?, ?)
        """, (
            int(sale_id),
            int(batch_id),
            int(qty),
            float(price)
        ))

        conn.commit()
        conn.close()

    # -----------------------------------
    # Перерахунок суми
    # -----------------------------------

    def update_total(self, sale_id: int):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE sales
            SET total_amount = IFNULL((
                SELECT SUM(quantity * price)
                FROM sale_items
                WHERE sale_id = ?
            ), 0)
            WHERE id = ?
        """, (int(sale_id), int(sale_id)))

        conn.commit()
        conn.close()

    # -----------------------------------
    # Список продажів (з іменем покупця)
    # -----------------------------------

    def list_all(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                si.id,
                m.name,
                b.batch_number,
                c.full_name,
                u.username,
                s.sale_date,
                b.expiration_date,
                si.quantity,
                si.price,
                si.quantity * si.price
            FROM sale_items si
            JOIN sales s ON s.id = si.sale_id
            JOIN batches b ON b.id = si.batch_id
            JOIN medicines m ON m.id = b.medicine_id
            JOIN customers c ON c.id = s.customer_id
            JOIN users u ON u.id = s.user_id
            ORDER BY s.sale_date DESC
        """)

        rows = cur.fetchall()
        conn.close()

        return rows

    # -----------------------------------
    # Деталі продажу (на майбутнє)
    # -----------------------------------

    def get_sale_items(self, sale_id: int):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                si.id,
                m.name,
                si.quantity,
                si.price,
                si.quantity * si.price as total
            FROM sale_items si
            JOIN batches b ON b.id = si.batch_id
            JOIN medicines m ON m.id = b.medicine_id
            WHERE si.sale_id = ?
        """, (int(sale_id),))

        rows = cur.fetchall()
        conn.close()

        return rows