import os
from cryptography.fernet import Fernet

def load_key(key_path):
    if os.path.exists(key_path):
        with open(key_path, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
        return key

def save_password(file_path, fernet, website, username, password):
    with open(file_path, "a") as file:
        encrypted = fernet.encrypt(f"{website} | {username} | {password}".encode())
        file.write(encrypted.decode() + "\n")

def view_passwords(file_path, fernet):
    if not os.path.exists(file_path):
        print("No password file found.")
        return

    with open(file_path, "r") as file:
        for line in file:
            try:
                decrypted = fernet.decrypt(line.strip().encode()).decode()
                print(decrypted)
            except:
                print("Decryption failed on one line.")

def main():
    file_path = input("Enter the password file path (e.g., /path/to/passwords.txt): ").strip()
    dir_path = os.path.dirname(file_path)
    key_path = os.path.join(dir_path, "key.key")
    key = load_key(key_path)
    fernet = Fernet(key)

    while True:
        choice = input("Choose an option: [add/view/exit]: ").strip().lower()
        if choice == "add":
            website = input("Website: ")
            username = input("Username: ")
            password = input("Password: ")
            save_password(file_path, fernet, website, username, password)
        elif choice == "view":
            view_passwords(file_path, fernet)
        elif choice == "exit":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()