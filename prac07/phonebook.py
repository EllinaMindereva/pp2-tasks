import psycopg2
import csv
import os
from config import h, db, u, p

conn = psycopg2.connect(
    host = h,
    database = db,
    user = u,
    password = p)

def create_table():
    command = """
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY, 
        user_name VARCHAR(255) NOT NULL,
        phone VARCHAR(12) NOT NULL
    )"""
    with conn.cursor() as cur:
            cur.execute(command)
    conn.commit()

def get_from_csv(filename):
    command = "INSERT INTO contacts(user_name, phone) VALUES(%s, %s)"
    with open(filename, "r") as f:
        r = csv.reader(f)
        with conn.cursor() as cur:
            for i in r:
                cur.execute(command, (i[0], i[1]))
            conn.commit()
    print("Data from the file was imported")

def get_from_console():
    command = "INSERT INTO contacts(user_name, phone) VALUES(%s, %s)"
    user_name = input("Input your user name: ")
    phone = input("Input your phone number: ")
    with conn.cursor() as cur:
        cur.execute(command, (user_name, phone))
        conn.commit()
    print("New contact was added")

def update_user(phone, new_username):
    command = "UPDATE contacts SET user_name = %s WHERE phone = %s"
    with conn.cursor() as cur:
        cur.execute(command, (new_username, phone))
        conn.commit()
    print("The user name was updated")

def update_phone(user_name, new_phone):
    command = "UPDATE contacts SET phone = %s WHERE user_name = %s"
    with conn.cursor() as cur:
        cur.execute(command, (new_phone, user_name))
        conn.commit()
    print("The phone number was updated")

def filter_name(find):
    command = "SELECT * FROM contacts WHERE user_name ILIKE %s"
    pattern = f"%{find}%"
    with conn.cursor() as cur:
        cur.execute(command, (pattern,))
        return cur.fetchall()

def all_contacts():
    command = "SELECT * FROM contacts ORDER BY user_name"
    with conn.cursor() as cur:
        cur.execute(command)
        return cur.fetchall()

def delete_name(name):
    command = "DELETE FROM contacts WHERE user_name = %s"
    with conn.cursor() as cur:
        cur.execute(command, (name,))
        conn.commit()
    print("The contact was deleted")

def print_contacts(contacts):
    if not contacts:
        print("No contacts")
        return
    for i in contacts:
        print(f"  [{i[0]}] {i[1]} - {i[2]}")

def main():
    create_table()
    while True:
        print("\n~~~ Phonebook ~~~")
        print("1) Add user from CSV")
        print("2) Add user from input")
        print("3) Update user by phone")
        print("4) Update user by username")
        print("5) Filter user by name")
        print("6) Delete user by name")
        print("7) All contacts")
        print("0) Exit")

        num = input("\nChoose number: ")

        if num == "1":
            get_from_csv("contacts.csv")
        elif num == "2":
            get_from_console()
        elif num == "3":
            phone = input("Phone: ")
            new_username = input("Input new name: ")
            update_user(phone, new_username)
        elif num == "4":
            user_name = input("Username: ")
            new_phone = input("Input new phone number: ")
            update_phone(user_name, new_phone)
        elif num == "5":
            find = input("Input text: ")
            print_contacts(filter_name(find))
        elif num == "6":
            name = input("Input username: ")
            delete_name(name)
        elif num == "7":
            print_contacts(all_contacts())
        elif num == "0":
            break
        else:
            print("Incorrect number")
    conn.close()
if __name__ == "__main__":
    main()