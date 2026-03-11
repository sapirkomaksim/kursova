from database.connection import get_connection
from models.category import Category


class CategoryRepository:

    # ----------------------------------------
    # Додати категорію
    # ----------------------------------------
    def add(self, name: str) -> int:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO categories(name) VALUES(?)",
            (name.strip(),)
        )

        conn.commit()
        category_id = cur.lastrowid
        conn.close()

        return category_id

    # ----------------------------------------
    # Отримати всі категорії
    # ----------------------------------------
    def list_all(self) -> list[Category]:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, name FROM categories ORDER BY name"
        )

        rows = cur.fetchall()
        conn.close()

        return [Category(*row) for row in rows]

    # ----------------------------------------
    # Отримати категорію по ID
    # ----------------------------------------
    def get_by_id(self, category_id: int) -> Category | None:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, name FROM categories WHERE id=?",
            (int(category_id),)
        )

        row = cur.fetchone()
        conn.close()

        return Category(*row) if row else None

    # ----------------------------------------
    # Оновити категорію
    # ----------------------------------------
    def update(self, category_id: int, name: str):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE categories SET name=? WHERE id=?",
            (name.strip(), int(category_id))
        )

        conn.commit()
        conn.close()

    # ----------------------------------------
    # Видалити категорію
    # ----------------------------------------
    def delete(self, category_id: int):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM categories WHERE id=?",
            (int(category_id),)
        )

        conn.commit()
        conn.close()

    # ----------------------------------------
    # Перевірити чи використовується
    # ----------------------------------------
    def is_used(self, category_id: int) -> bool:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT COUNT(*) FROM medicines WHERE category_id=?",
            (int(category_id),)
        )

        count = cur.fetchone()[0]
        conn.close()

        return count > 0