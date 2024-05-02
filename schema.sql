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
    url TEXT NOT NULL,
    image_url TEXT NOT NULL,
    in_stock BOOLEAN
);

CREATE TABLE subscriptions (
    sub_id SERIAL PRIMARY KEY,
    user_id INT,
    plant_id INT,
    sub_added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (plant_id) REFERENCES plants(plant_id)
);

CREATE TABLE prices (
    price_id SERIAL PRIMARY KEY,
    price DECIMAL NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    plant_id INT,
    FOREIGN KEY (plant_id) REFERENCES plants(plant_id)
)