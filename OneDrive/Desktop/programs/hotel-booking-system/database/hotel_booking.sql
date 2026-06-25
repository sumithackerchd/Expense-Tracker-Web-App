CREATE DATABASE hotel_booking;

USE hotel_booking;

CREATE TABLE users(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hotels(
    id INT PRIMARY KEY AUTO_INCREMENT,
    hotel_name VARCHAR(200) NOT NULL,
    city VARCHAR(100),
    address TEXT,
    description TEXT,
    rating FLOAT DEFAULT 0,
    image VARCHAR(255)
);

CREATE TABLE rooms(
    id INT PRIMARY KEY AUTO_INCREMENT,
    hotel_id INT,
    room_type VARCHAR(100),
    price DECIMAL(10,2),
    capacity INT,
    available_rooms INT,
    image VARCHAR(255),

    FOREIGN KEY(hotel_id)
    REFERENCES hotels(id)
    ON DELETE CASCADE
);

CREATE TABLE bookings(
    id INT PRIMARY KEY AUTO_INCREMENT,

    user_id INT,
    room_id INT,

    checkin_date DATE,
    checkout_date DATE,

    guests INT,

    amount DECIMAL(10,2),

    payment_status VARCHAR(50) DEFAULT 'Pending',

    booking_status VARCHAR(50) DEFAULT 'Booked',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
    REFERENCES users(id)
    ON DELETE CASCADE,

    FOREIGN KEY(room_id)
    REFERENCES rooms(id)
    ON DELETE CASCADE
);