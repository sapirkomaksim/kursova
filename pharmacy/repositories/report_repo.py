from database.connection import get_connection


class ReportRepository:

    # -----------------------------
    # Продажі за період
    # -----------------------------
    def sales_report(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT
            s.sale_date,
            m.name,
            b.batch_number,
            c.full_name,
            u.username,
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

    # -----------------------------
    # Залишки складу
    # -----------------------------
    def stock_report(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT
            m.name,
            b.batch_number,
            s.name,
            b.expiration_date,
            b.quantity,
            b.purchase_price,
            b.quantity * b.purchase_price
        FROM batches b
        JOIN medicines m ON m.id = b.medicine_id
        JOIN suppliers s ON s.id = b.supplier_id
        WHERE b.quantity > 0
        ORDER BY m.name
        """)

        rows = cur.fetchall()
        conn.close()

        return rows

    # -----------------------------
    # Прострочені препарати
    # -----------------------------
    def expired_report(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT
            m.name,
            b.batch_number,
            s.name,
            b.expiration_date,
            b.quantity
        FROM batches b
        JOIN medicines m ON m.id = b.medicine_id
        JOIN suppliers s ON s.id = b.supplier_id
        WHERE b.expiration_date < date('now')
        AND b.quantity > 0
        ORDER BY b.expiration_date
        """)

        rows = cur.fetchall()
        conn.close()

        return rows

    # -----------------------------
    # Топ продажів
    # -----------------------------
    def top_sales_report(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT
            m.name,
            SUM(si.quantity),
            SUM(si.quantity * si.price)
        FROM sale_items si
        JOIN batches b ON b.id = si.batch_id
        JOIN medicines m ON m.id = b.medicine_id
        GROUP BY m.name
        ORDER BY SUM(si.quantity) DESC
        """)

        rows = cur.fetchall()
        conn.close()

        return rows