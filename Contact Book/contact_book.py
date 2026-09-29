"""
Contact Book
CRUD application with JSON and CSV file storage.
"""

import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
JSON_FILE = BASE_DIR / "data" / "contacts.json"
CSV_FILE = BASE_DIR / "data" / "contacts.csv"


def ensure_data_folder():
    JSON_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_contacts():
    ensure_data_folder()
    if not JSON_FILE.exists():
        return []
    try:
        with JSON_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_contacts(contacts):
    ensure_data_folder()
    with JSON_FILE.open("w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)


def export_csv(contacts):
    ensure_data_folder()
    fields = ["id", "name", "phone", "email", "address"]

    with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(contacts)

    print(f"Contacts exported to {CSV_FILE.name}.")


def next_id(contacts):
    return max((contact["id"] for contact in contacts), default=0) + 1


def find_contact(contacts, contact_id):
    try:
        contact_id = int(contact_id)
    except ValueError:
        return None
    return next((c for c in contacts if c["id"] == contact_id), None)


def add_contact(contacts):
    print("\n--- Add Contact ---")
    name = input("Name: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    address = input("Address: ").strip()

    if not name or not phone:
        print("Name and phone are required.")
        return

    contact = {
        "id": next_id(contacts),
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
    }

    contacts.append(contact)
    save_contacts(contacts)
    print("Contact added successfully.")


def view_contacts(contacts):
    print("\n--- Contact List ---")

    if not contacts:
        print("No contacts found.")
        return

    print(f"{'ID':<5}{'Name':<22}{'Phone':<16}{'Email':<28}")
    print("-" * 71)

    for contact in contacts:
        print(
            f"{contact['id']:<5}"
            f"{contact['name'][:20]:<22}"
            f"{contact['phone'][:14]:<16}"
            f"{contact['email'][:26]:<28}"
        )


def view_contact_details(contacts):
    contact = find_contact(contacts, input("Enter contact ID: ").strip())

    if not contact:
        print("Contact not found.")
        return

    print("\n--- Contact Details ---")
    for key, value in contact.items():
        print(f"{key.title():<10}: {value}")


def update_contact(contacts):
    contact = find_contact(contacts, input("Enter contact ID to update: ").strip())

    if not contact:
        print("Contact not found.")
        return

    print("Press ENTER to keep the existing value.")
    for field in ["name", "phone", "email", "address"]:
        value = input(f"{field.title()} [{contact[field]}]: ").strip()
        if value:
            contact[field] = value

    if not contact["name"] or not contact["phone"]:
        print("Name and phone are required.")
        return

    save_contacts(contacts)
    print("Contact updated successfully.")


def delete_contact(contacts):
    contact = find_contact(contacts, input("Enter contact ID to delete: ").strip())

    if not contact:
        print("Contact not found.")
        return

    confirm = input(f"Delete {contact['name']}? (y/n): ").strip().lower()

    if confirm == "y":
        contacts.remove(contact)
        save_contacts(contacts)
        print("Contact deleted successfully.")
    else:
        print("Delete cancelled.")


def search_contacts(contacts):
    query = input("Search by name, phone, or email: ").strip().lower()

    matches = [
        contact for contact in contacts
        if query in contact["name"].lower()
        or query in contact["phone"].lower()
        or query in contact["email"].lower()
    ]

    if not matches:
        print("No matching contacts found.")
        return

    print(f"\nFound {len(matches)} contact(s):")
    for contact in matches:
        print(
            f"ID: {contact['id']} | "
            f"{contact['name']} | "
            f"{contact['phone']} | "
            f"{contact['email']}"
        )


def main():
    contacts = load_contacts()

    while True:
        print("\n" + "=" * 55)
        print(" CONTACT BOOK")
        print("=" * 55)
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. View Contact Details")
        print("4. Search Contacts")
        print("5. Update Contact")
        print("6. Delete Contact")
        print("7. Export to CSV")
        print("8. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            view_contact_details(contacts)
        elif choice == "4":
            search_contacts(contacts)
        elif choice == "5":
            update_contact(contacts)
        elif choice == "6":
            delete_contact(contacts)
        elif choice == "7":
            export_csv(contacts)
        elif choice == "8":
            print("Thank you for using Contact Book.")
            break
        else:
            print("Invalid choice. Please select 1-8.")


if __name__ == "__main__":
    main()
