CREATE OR REPLACE PROCEDURE upsert_user(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_users(users TEXT[][])
LANGUAGE plpgsql
AS $$
DECLARE
    user_record TEXT[];
    invalid_data TEXT[] := '{}';
BEGIN
    FOREACH user_record SLICE 1 IN ARRAY users LOOP
        IF user_record[2] ~ '^\d+$' THEN
            PERFORM upsert_user(user_record[1], user_record[2]);
        ELSE
            invalid_data := array_append(invalid_data, user_record[1] || ':' || user_record[2]);
        END IF;
    END LOOP;

    IF array_length(invalid_data,1) > 0 THEN
        RAISE NOTICE 'Invalid users: %', invalid_data;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_user(p_name VARCHAR DEFAULT NULL, p_phone VARCHAR DEFAULT NULL)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE (p_name IS NOT NULL AND first_name = p_name)
       OR (p_phone IS NOT NULL AND phone = p_phone);
END;
$$;