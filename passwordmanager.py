import os
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from getpass import getpass
from typing import Optional


def load_or_create_key(key_path: Path) -> bytes:
    key_path.parent.mkdir(parents=True, exist_ok=True)

    if key_path.exists():
        return key_path.read_bytes()

    key = Fernet.generate_key()
    key_path.write_bytes(key)

    # Restrict permissions (important on Unix systems)
    try:
        os.chmod(key_path, 0o600)
    except Exception:
        pass

    return key


def encrypt_entry(fernet: Fernet, website: str, username: str, password: str) -> str:
    data = f"{website}|{username}|{password}".encode()
    return fernet.encrypt(data).decode()


def decrypt_entry(fernet: Fernet, token: str) -> Optional[str]:
    try:
        return fernet.decrypt(token.encode()).decode()
    except InvalidToken:
        return None


def save_password(file_path: Path, fernet: Fernet):
    website = input("Website: ").strip()
    username = input("Username: ").strip()
    password = getpass("Password (hidden): ").strip()

    encrypted = encrypt_entry(fernet, website, username, password)

    with file_path.open("a") as f:
        f.write(encrypted + "\n")

    print("✅ Password saved securely.")


def view_passwords(file_path: Path, fernet: Fernet):
    if not file_path.exists():
        print("No password file found.")
        return

    print("\n🔐 Stored Credentials:\n" + "-" * 30)

    with file_path.open("r") as f:
        for i, line in enumerate(f, 1):
            decrypted = decrypt_entry(fernet, line.strip())
            if decrypted:
                website, username, password = decrypted.split("|")
                print(f"{i}. {website} | {username} | {password}")
            else:
                print(f"{i}. ⚠️ Corrupted or invalid entry")

    print("-" * 30)


def search_password(file_path: Path, fernet: Fernet):
    query = input("Search website: ").strip().lower()

    if not file_path.exists():
        print("No password file found.")
        return

    found = False

    with file_path.open("r") as f:
        for line in f:
            decrypted = decrypt_entry(fernet, line.strip())
            if decrypted:
                website, username, password = decrypted.split("|")
                if query in website.lower():
                    print(f"{website} | {username} | {password}")
                    found = True

    if not found:
        print("No matching entries found.")


def main():
    base_dir = Path.home() / ".password_manager"
    file_path = base_dir / "passwords.txt"
    key_path = base_dir / "key.key"

    key = load_or_create_key(key_path)
    fernet = Fernet(key)

    actions = {
        "add": save_password,
        "view": view_passwords,
        "search": search_password,
    }

    while True:
        choice = input("\nChoose [add/view/search/exit]: ").strip().lower()

        if choice == "exit":
            print("Goodbye.")
            break

        action = actions.get(choice)
        if action:
            action(file_path, fernet)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
