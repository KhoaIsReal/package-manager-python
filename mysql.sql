CREATE DATABASE pm_db;

USE pm_db;

CREATE TABLE file_infomation(
	id INT AUTO_INCREMENT PRIMARY KEY,
    _description TINYTEXT,
    file_name VARCHAR(50)
);