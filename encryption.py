from cryptography.fernet import Fernet
import os

# Cale unde salvez cheia de criptare
KEY_FILE = "encryption.key"

def generate_key():
    """
    Generează o cheie de criptare unică.
    Se apelează o singură dată!
    """
    key = Fernet.generate_key()
    
    # Salvez cheia în fișierul encryption.key
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    
    print("✅ Cheie de criptare generată și salvată!")
    return key


def load_key():
    """
    Încarc cheia de criptare din fișier.
    """
    if not os.path.exists(KEY_FILE):
        print("⚠️ Cheie nu găsită! Generez una nouă...")
        return generate_key()
    
    with open(KEY_FILE, "rb") as key_file:
        key = key_file.read()
    
    return key


def encrypt_password(password):
    """
    Criptează o parolă folosind cheia salvată.
    Returnează parola criptată (bytes).
    """
    key = load_key()
    cipher = Fernet(key)
    
    # Criptează parola
    encrypted = cipher.encrypt(password.encode())
    
    return encrypted.decode()  # Returnez ca string


def decrypt_password(encrypted_password):
    """
    Decriptează o parolă salvată.
    Returnează parola originală (text).
    """
    key = load_key()
    cipher = Fernet(key)
    
    # Decriptează parola
    decrypted = cipher.decrypt(encrypted_password.encode())
    
    return decrypted.decode()  # Returnez ca string


# Test
if __name__ == "__main__":
    # Test 1: Generez o cheie (se întâmplă o dată)
    generate_key()
    
    # Test 2: Criptez o parolă
    parola_originala = "gmail_password_123!"
    parola_criptata = encrypt_password(parola_originala)
    print(f"Parola originală: {parola_originala}")
    print(f"Parola criptată: {parola_criptata}")
    
    # Test 3: Decriptez parola
    parola_decriptata = decrypt_password(parola_criptata)
    print(f"Parola decriptată: {parola_decriptata}")
    
    # Test 4: Verific dacă e aceeași
    if parola_decriptata == parola_originala:
        print("✅ Criptare și decriptare funcționează perfect!")
    else:
        print("❌ Ceva nu e bine!")