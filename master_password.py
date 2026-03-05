import sqlite3
import bcrypt
from database import init_db

def save_master_password(password):
    """
    Salvează master password-ul hash-at în baza de date.
    Se apelează o singură dată la prima pornire.
    """
    # Conectează la baza de date
    conn = init_db()
    cursor = conn.cursor()
    
    # Hash-ează parola
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt).decode()
    
    # Salvează în baza de date (într-un tabel separat)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS master_password (
            id INTEGER PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    """)
    
    # Ștergem orice master password vechi
    cursor.execute("DELETE FROM master_password")
    
    # Inserează noul master password
    cursor.execute(
        "INSERT INTO master_password (password_hash) VALUES (?)",
        (hashed,)
    )
    
    conn.commit()
    conn.close()
    print("✅ Master password salvat cu succes!")


def get_master_password_hash():
    """
    Preiau hash-ul master password-ului din baza de date.
    """
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT password_hash FROM master_password LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    else:
        return None


def verify_master_password(password):
    """
    Verifică dacă parola introdusă se potrivește cu master password-ul salvat.
    """
    hashed = get_master_password_hash()
    
    if hashed is None:
        return False
    
    return bcrypt.checkpw(password.encode(), hashed.encode())


def is_master_password_set():
    """
    Verifică dacă master password-ul a fost deja setat.
    """
    return get_master_password_hash() is not None

# Test
if __name__ == "__main__":
    # Test 1: Salvează master password
    save_master_password("MyMasterPassword123!")
    
    # Test 2: Verifică dacă e salvat
    if is_master_password_set():
        print("✅ Master password e setat!")
    
    # Test 3: Verifică dacă parola corectă merge
    if verify_master_password("MyMasterPassword123!"):
        print("✅ Master password verificat corect!")
    else:
        print("❌ Master password greșit!")
    
    # Test 4: Verifică dacă parola greșită e detectată
    if verify_master_password("WrongPassword"):
        print("❌ Asta nu ar trebui să apară!")
    else:
        print("✅ Parola greșită detectată!")