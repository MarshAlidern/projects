import csv
from connect import connect 
from config import load_config

config = load_config()

def create_table():
    conn = connect(config)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            phone VARCHAR(20) UNIQUE NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect(config)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()


def insert_from_csv(filename):
    conn = connect(config)
    cur = conn.cursor()

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                (row[0], row[1])
            )

    conn.commit()
    cur.close()
    conn.close()



def update_contact():
    old_name = input("Enter existing name: ")
    new_name = input("New name (Enter to skip): ")
    new_phone = input("New phone (Enter to skip): ")

    conn = connect(config)
    cur = conn.cursor()

    if new_name:
        cur.execute(
            "UPDATE phonebook SET first_name = %s WHERE first_name = %s",
            (new_name, old_name)
        )

    if new_phone:
        cur.execute(
            "UPDATE phonebook SET phone = %s WHERE first_name = %s",
            (new_phone, old_name)
        )

    conn.commit()
    cur.close()
    conn.close()



def search_by_name():
    name = input("Enter name: ")

    conn = connect(config)
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE first_name ILIKE %s",
        (f"%{name}%",)
    )

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def search_by_phone():
    prefix = input("Enter phone prefix: ")

    conn = connect(config)
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE phone LIKE %s",
        (f"{prefix}%",)
    )

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()



def delete_contact():
    choice = input("Delete by (1) name or (2) phone: ")

    conn = connect(config)
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
    elif choice == "2":
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))

    conn.commit()
    cur.close()
    conn.close()


def menu():
    create_table()

    while True:
        print("\n1. Add from console")
        print("2. Import from CSV")
        print("3. Update contact")
        print("4. Search by name")
        print("5. Search by phone prefix")
        print("6. Delete contact")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_from_console()
        elif choice == "2":
            insert_from_csv("contacts.csv")
        elif choice == "3":
            update_contact()
        elif choice == "4":
            search_by_name()
        elif choice == "5":
            search_by_phone()
        elif choice == "6":
            delete_contact()
        elif choice == "0":
            break


if __name__ == "__main__":
    menu()