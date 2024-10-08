-- Task 8: Optimizing simple search
-- on the table names
CREATE INDEX idx_name_first ON names ( name(1) );
