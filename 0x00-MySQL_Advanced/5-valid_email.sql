  
-- Task-5: Email validation to be sent - will create a trigger that resets the attr valid_email
-- only if the email has been changed
DELIMITER |
CREATE TRIGGER email_bool BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
    SET NEW.valid_email = 0;
    END IF;
END;
|
