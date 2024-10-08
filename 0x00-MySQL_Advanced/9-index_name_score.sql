-- Task 9: Optimize search and score
-- first letter of name & the score
CREATE INDEX idx_name_first_score ON names ( name(1), score );
