import bcrypt

def hash_password(password):
    #Genereaza un salt
    salt = bcrypt.gensalt()

    #Combina parola cu saltul pentru un hash
    hashed = bcrypt.hashpw(password.encode(), salt)

    #Returneaza hashul
    return hashed.decode()

def verify_password(password, hashed_password):
    """
    Compara parola cu hashul 
    Returneaza true daca se potrivesc si false altfel
    """

    return bcrypt.checkpw(password.encode(), hashed_password.encode())

# Testez funcțiile
if __name__ == "__main__":
    # Test 1: Hash o parolă
    parola_original = "MySecurePassword123!"
    hash_parola = hash_password(parola_original)
    print(f"Parola originală: {parola_original}")
    print(f"Hash-ul: {hash_parola}")
    
    # Test 2: Verifică dacă parola corectă se potrivește
    if verify_password(parola_original, hash_parola):
        print("✅ Parola corectă!")
    else:
        print("❌ Parola greșită!")
    
    # Test 3: Verifică dacă o parolă greșită nu se potrivește
    if verify_password("WrongPassword", hash_parola):
        print("❌ Asta nu ar trebui să se afișeze!")
    else:
        print("✅ Parola greșită detectată corect!")