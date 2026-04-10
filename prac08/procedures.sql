CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR) AS $$
BEGIN 
    IF EXISTS (SELECT 1 FROM contacts WHERE user_name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE user_name = p_name;
    ELSE
        INSERT INTO contacts(user_name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE insert_many(user_names VARCHAR[], phones VARCHAR[]) AS $$
DECLARE
    i INTEGER;
BEGIN
    FOR i IN 1..array_length(user_names, 1) LOOP
        IF phones[i] ~ "^[0-9]+$" THEN
            INSERT INTO contacts(user_name, phone)
            VALUES(user_names[i], phones[i])
        ELSE
            RAISE NOTICE "invalid phone number: % for user: %", user_names[i], phones[i];
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_contact(p_val text) AS $$
BEGIN 
    DELETE FROM contacts WHERE user_name = p_val OR phone = p_val;
END;
$$ LANGUAGE plpgsql;

