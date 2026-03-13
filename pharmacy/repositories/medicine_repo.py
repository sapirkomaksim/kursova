from database.connection import get_connection
from models.medicine import Medicine


class MedicineRepository:

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

        conn = get_connection()
        cur = conn.cursor()

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

        conn.commit()
        med_id = cur.lastrowid
        conn.close()
        return med_id

    # ---------------------- LIST ALL (JOIN categories) ----------------------

    def list_all(self) -> list[Medicine]:

        conn = get_connection()
        cur = conn.cursor()

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
        conn.close()

        medicines = []

        for row in rows:
            medicines.append(
                Medicine(
                    id=row[0],
                    name=row[1],
                    manufacturer=row[2],
                    category_id=row[3],
                    prescription_required=bool(row[4]),
                    retail_price=row[5],
                    category_name=row[6]   # 🔥 важливо
                )
            )

        return medicines

    # ---------------------- GET BY ID (JOIN) ----------------------

    def get_by_id(self, med_id: int) -> Medicine | None:

        conn = get_connection()
        cur = conn.cursor()

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
        conn.close()

        if not row:
            return None

        return Medicine(
            id=row[0],
            name=row[1],
            manufacturer=row[2],
            category_id=row[3],
            prescription_required=bool(row[4]),
            retail_price=row[5],
            category_name=row[6]   # 🔥 важливо
        )

    # ---------------------- UPDATE PRICE ----------------------

    def update_price(self, medicine_id: int, new_price: float) -> None:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE medicines SET retail_price=? WHERE id=?",
            (float(new_price), int(medicine_id))
        )

        conn.commit()
        conn.close()

    # ---------------------- DELETE ----------------------

    def delete(self, med_id: int) -> None:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM medicines WHERE id=?", (int(med_id),))

        conn.commit()
        conn.close()

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

        conn = get_connection()
        cur = conn.cursor()

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

        conn.commit()
        conn.close()