import sqlite3
from database import init_db
from encryption import encrypt_password, decrypt_password

def add_password(website, username, password):
    """
    Adaugă o parolă criptată în baza de date.
    """
    conn = init_db()
    cursor = conn.cursor()
    
    # Criptez parola
    encrypted = encrypt_password(password)
    
    # Inserez în tabelul vault
    cursor.execute(
        "INSERT INTO vault (website, username, password) VALUES (?, ?, ?)",
        (website, username, encrypted)
    )
    
    conn.commit()
    conn.close()
    print(f"✅ Parolă salvată pentru {website}")


def get_password(website):
    """
    Preiau o parolă din baza de date și o decriptez.
    """
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT username, password FROM vault WHERE website = ?",
        (website,)
    )
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        username, encrypted_password = result
        decrypted = decrypt_password(encrypted_password)
        return {"website": website, "username": username, "password": decrypted}
    else:
        return None


def get_all_passwords():
    """
    Preiau TOATE parolele și le decriptez.
    """
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, website, username, password FROM vault")
    
    results = cursor.fetchall()
    conn.close()
    
    passwords = []
    for row in results:
        id, website, username, encrypted_password = row
        decrypted = decrypt_password(encrypted_password)
        passwords.append({
            "id": id,
            "website": website,
            "username": username,
            "password": decrypted
        })
    
    return passwords


def delete_password(website):
    """
    Șterge o parolă din baza de date.
    """
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM vault WHERE website = ?", (website,))
    
    conn.commit()
    conn.close()
    print(f"✅ Parolă pentru {website} ștearsă")


def search_passwords(search_term):
    """
    Caută parole după website sau username.
    """
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, website, username, password FROM vault WHERE website LIKE ? OR username LIKE ?",
        (f"%{search_term}%", f"%{search_term}%")
    )
    
    results = cursor.fetchall()
    conn.close()
    
    passwords = []
    for row in results:
        id, website, username, encrypted_password = row
        decrypted = decrypt_password(encrypted_password)
        passwords.append({
            "id": id,
            "website": website,
            "username": username,
            "password": decrypted
        })
    
    return passwords

# Test
if __name__ == "__main__":
    # Test 1: Adaug o parolă
    add_password("gmail.com", "john@gmail.com", "SecurePassword123!")
    add_password("facebook.com", "john_doe", "FacebookPass456!")
    
    # Test 2: Preiau o parolă
    result = get_password("gmail.com")
    print(f"Gmail: {result}")
    
    # Test 3: Preiau toate parolele
    all_passwords = get_all_passwords()
    print(f"\nTote parolele:")
    for pwd in all_passwords:
        print(f"  - {pwd['website']}: {pwd['username']}")
    
    # Test 4: Caut
    search_result = search_passwords("john")
    print(f"\nCautare 'john': {len(search_result)} rezultate")
    
    # Test 5: Șterg
    delete_password("facebook.com")
    
    # Test 6: Verific că e ștearsă
    all_passwords = get_all_passwords()
    print(f"\nDupă ștergere: {len(all_passwords)} parole")