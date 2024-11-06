-- Creating permissions for database and user
CREATE DATABASE IF NOT EXISTS hbnb_evo_2_db;
CREATE USER IF NOT EXISTS 'hbnb_evo_2_db'@'localhost' IDENTIFIED BY '123';
GRANT ALL PRIVILEGES ON hbnb_evo_2_db.* TO 'hbnb_evo_2_db'@'localhost';
FLUSH PRIVILEGES;
SELECT user, host FROM mysql.user WHERE user='hbnb_evo_2_db';
SHOW GRANTS FOR 'hbnb_evo_2_db'@'localhost';
