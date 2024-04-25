DROP DATABASE IF EXISTS flora_fare;
CREATE DATABASE flora_fare;

\c flora_fare;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(25) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE plants (
    plant_id SERIAL PRIMARY KEY,
    plant_name TEXT UNIQUE NOT NULL,
    original_price DECIMAL,
    curr_price DECIMAL,
    url TEXT UNIQUE NOT NULL,
    image_url TEXT UNIQUE NOT NULL,
    in_stock BOOLEAN
)