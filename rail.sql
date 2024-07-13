-- Create a new database
CREATE DATABASE IF NOT EXISTS train_details_db;
USE train_details_db;

-- Create a table for train details
CREATE TABLE IF NOT EXISTS train_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    train_name VARCHAR(255) NOT NULL,
    departure_city VARCHAR(255) NOT NULL,
    arrival_city VARCHAR(255) NOT NULL
);
