-- Task 1: 1-country_users.sql In & not out - This will create a table of usrs
-- The script can be exe on any db
CREATE TABLE IF NOT EXISTS `users` (  
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `name` VARCHAR(255),
    `country` ENUM('US', 'CO', 'TN') NOT NULL 
)
