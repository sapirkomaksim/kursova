from models.medicine import Medicine


class MedicineRepository:

    def __init__(self, conn=None):
        from database.connection import get_connection
        self.conn = conn or get_connection()

    # ---------------------- ADD ----------------------

    def add(
        self,
        name: str,
        manufacturer: str | None,
        category_id: int | None,
        prescription_required: bool,
        retail_price: float
    ) -> int:

        if retail_price < 0:
            raise ValueError("Ціна не може бути від'ємною")

        cur = self.conn.cursor()

        cur.execute(
            """
            INSERT INTO medicines(name, manufacturer, category_id,
                                  prescription_required, retail_price)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                name.strip(),
                manufacturer.strip() if manufacturer else None,
                category_id,
                int(prescription_required),
                float(retail_price)
            )
        )

        self.conn.commit()
        return cur.lastrowid

    # ---------------------- LIST ALL ----------------------

    def list_all(self) -> list[Medicine]:

        cur = self.conn.cursor()

        cur.execute("""
            SELECT
                m.id,
                m.name,
                m.manufacturer,
                m.category_id,
                m.prescription_required,
                m.retail_price,
                c.name AS category_name
            FROM medicines m
            LEFT JOIN categories c ON c.id = m.category_id
            ORDER BY m.name
        """)

        rows = cur.fetchall()

        return [
            Medicine(
                id=row[0],
                name=row[1],
                manufacturer=row[2],
                category_id=row[3],
                prescription_required=bool(row[4]),
                retail_price=row[5],
                category_name=row[6]
            )
            for row in rows
        ]

    # ---------------------- GET BY ID ----------------------

    def get_by_id(self, med_id: int) -> Medicine | None:

        cur = self.conn.cursor()

        cur.execute("""
            SELECT
                m.id,
                m.name,
                m.manufacturer,
                m.category_id,
                m.prescription_required,
                m.retail_price,
                c.name AS category_name
            FROM medicines m
            LEFT JOIN categories c ON c.id = m.category_id
            WHERE m.id=?
        """, (int(med_id),))

        row = cur.fetchone()

        if not row:
            return None

        return Medicine(
            id=row[0],
            name=row[1],
            manufacturer=row[2],
            category_id=row[3],
            prescription_required=bool(row[4]),
            retail_price=row[5],
            category_name=row[6]
        )

    # ---------------------- UPDATE PRICE ----------------------

    def update_price(self, medicine_id: int, new_price: float) -> None:

        if new_price < 0:
            raise ValueError("Ціна не може бути від'ємною")

        cur = self.conn.cursor()

        cur.execute(
            "UPDATE medicines SET retail_price=? WHERE id=?",
            (float(new_price), int(medicine_id))
        )

        self.conn.commit()

    # ---------------------- DELETE ----------------------

    def delete(self, med_id: int) -> None:

        cur = self.conn.cursor()

        cur.execute(
            "DELETE FROM medicines WHERE id=?",
            (int(med_id),)
        )

        self.conn.commit()

    # ---------------------- UPDATE FULL ----------------------

    def update(
        self,
        med_id: int,
        name: str,
        manufacturer: str | None,
        category_id: int | None,
        prescription_required: bool,
        retail_price: float
    ) -> None:

        if retail_price < 0:
            raise ValueError("Ціна не може бути від'ємною")

        cur = self.conn.cursor()

        cur.execute("""
            UPDATE medicines
            SET name=?,
                manufacturer=?,
                category_id=?,
                prescription_required=?,
                retail_price=?
            WHERE id=?
        """, (
            name.strip(),
            manufacturer.strip() if manufacturer else None,
            category_id,
            int(prescription_required),
            float(retail_price),
            int(med_id)
        ))

        self.conn.commit()