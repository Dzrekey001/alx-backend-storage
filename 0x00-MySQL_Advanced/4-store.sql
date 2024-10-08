-- Task 4: Buy - will create a trigger that decreases the qty
-- of the item after adding with a new order
CREATE TRIGGER order_decrease BEFORE INSERT ON orders
FOR EACH ROW UPDATE items
SET quantity = quantity - NEW.number
WHERE name = NEW.item_name;
