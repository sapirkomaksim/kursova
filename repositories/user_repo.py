from database.connection import get_connection
from models.user import User


class UserRepository:
    def add(self, username: str, password_hash: str, role_id: int) -> int:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users(username, password_hash, role_id) VALUES(?, ?, ?)",
            (username.strip(), password_hash, int(role_id))
        )

        conn.commit()
        uid = cur.lastrowid
        conn.close()
        return uid

    def list_all(self) -> list[User]:
        """Повертає всіх користувачів разом із назвою ролі (JOIN roles)."""
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT u.id,
                   u.username,
                   u.password_hash,
                   u.role_id,
                   u.created_at,
                   r.name
            FROM users u
            JOIN roles r ON u.role_id = r.id
            ORDER BY u.username
        """)
        rows = cur.fetchall()
        conn.close()

        return [User(*row) for row in rows]

    def get_by_username(self, username: str) -> User | None:
        """Пошук користувача по username разом із назвою ролі."""
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT u.id,
                   u.username,
                   u.password_hash,
                   u.role_id,
                   u.created_at,
                   r.name
            FROM users u
            JOIN roles r ON u.role_id = r.id
            WHERE u.username = ?
        """, (username.strip(),))

        row = cur.fetchone()
        conn.close()

        return User(*row) if row else None

    def get_by_id(self, user_id: int) -> User | None:
        """Пошук користувача по id (з роллю)."""
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT u.id,
                   u.username,
                   u.password_hash,
                   u.role_id,
                   u.created_at,
                   r.name
            FROM users u
            JOIN roles r ON u.role_id = r.id
            WHERE u.id = ?
        """, (int(user_id),))

        row = cur.fetchone()
        conn.close()

        return User(*row) if row else None

    def update_password(self, user_id: int, new_password_hash: str) -> None:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE users SET password_hash=? WHERE id=?",
            (new_password_hash, int(user_id))
        )

        conn.commit()
        conn.close()

    def update_role(self, user_id: int, role_id: int) -> None:
        """Адмінська операція: змінити роль користувачу."""
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE users SET role_id=? WHERE id=?",
            (int(role_id), int(user_id))
        )

        conn.commit()
        conn.close()

    def delete(self, user_id: int) -> None:
        """Видалення користувача по id."""
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM users WHERE id=?", (int(user_id),))

        conn.commit()
        conn.close()