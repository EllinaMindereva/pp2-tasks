CREATE OR REPLACE FUNCTION return_matches(p text)
RETURNS TABLE(id INTEGER, user_name VARCHAR(255), phone VARCHAR(12)) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM contacts
    WHERE contacts.user_name ILIKE '%' || p || '%'
        OR contacts.phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;

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
