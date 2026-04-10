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

create_f_return_matches = """
    CREATE OR REPLACE FUNCTION return_matches(p text)
    RETURNS TABLE(id INTEGER, user_name VARCHAR(255), phone VARCHAR(12)) AS $$
    BEGIN
        RETURN QUERY
        SELECT * FROM contacts
        WHERE contacts.user_name ILIKE '%' || p || '%'
            OR contacts.phone ILIKE '%' || p || '%';
    END;
    $$ LANGUAGE plpgsql;
"""
create_f_pagination = """
    CREATE OR REPLACE FUNCTION pagination(page_limit INTEGER, page_offset INTEGER)
    RETURNS TABLE(id INTEGER, user_name VARCHAR(255), phone VARCHAR(12)) AS $$
    BEGIN
        RETURN QUERY
        SELECT * FROM contacts
        ORDER BY contacts.id
        LIMIT page_limit
        OFFSET page_offset;
    END;
    $$ LANGUAGE plpgsql;
"""
create_p_upsert_contact = """
    CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR) AS $$
    BEGIN 
        IF EXISTS (SELECT 1 FROM contacts WHERE user_name = p_name) THEN
            UPDATE contacts SET phone = p_phone WHERE user_name = p_name;
        ELSE
            INSERT INTO contacts(user_name, phone) VALUES(p_name, p_phone);
        END IF;
    END;
    $$ LANGUAGE plpgsql;
"""
create_p_insert_many = """
    CREATE OR REPLACE PROCEDURE insert_many(user_names VARCHAR[], phones VARCHAR[]) AS $$
    DECLARE
        i INTEGER;
    BEGIN
        FOR i IN 1..array_length(user_names, 1) LOOP
            IF phones[i] ~ '^[0-9]+$' THEN
                INSERT INTO contacts(user_name, phone)
                VALUES(user_names[i], phones[i]);
            ELSE
                RAISE NOTICE 'Invalid phone: % for user: %', phones[i], user_names[i];
            END IF;
        END LOOP;
    END;
    $$ LANGUAGE plpgsql;
"""
create_p_delete_contact = """
    CREATE OR REPLACE PROCEDURE delete_contact(p_val text) AS $$
    BEGIN 
        DELETE FROM contacts WHERE user_name = p_val OR phone = p_val;
    END;
    $$ LANGUAGE plpgsql;
"""

def execute(query):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
      
def main():
    create_table()
    while True:
        print("\n~~~ Phonebook ~~~")
        print("1) functions and procedures")
        print("0) exit")

        num = input("\nChoose number: ")

        if num == "1":
            execute(create_f_return_matches)
            execute(create_f_pagination)
            execute(create_p_upsert_contact)
            execute(create_p_insert_many)
            execute(create_p_delete_contact)
        elif num == "0":
            break
        else:
            print("Incorrect number")
    conn.close()
if __name__ == "__main__":
    main()