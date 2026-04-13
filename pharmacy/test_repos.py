# rehash_users.py
import hashlib
from database.connection import get_connection

# Задай тут паролі, які хочеш встановити
NEW_PASSWORDS = {
    "admin": "admin",
    "pharma1": "pass",
}

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()

def rehash_users():
    conn = get_connection()
    cur = conn.cursor()

    for username, plain in NEW_PASSWORDS.items():
        new_hash = sha256_hex(plain)
        cur.execute(
            "UPDATE users SET password_hash=? WHERE username=?",
            (new_hash, username)
        )

    conn.commit()
    conn.close()
    print("✅ Passwords rehashed for:", ", ".join(NEW_PASSWORDS.keys()))

if __name__ == "__main__":
    rehash_users()