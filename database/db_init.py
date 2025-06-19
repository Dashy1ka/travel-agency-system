from datetime import datetime

import sqlite3

def create_tables():
    conn = sqlite3.connect('travel_agency.db')
    cursor = conn.cursor()

    # Таблица клиентов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            passport TEXT,
            phone TEXT,
            email TEXT,
            preferences TEXT,
            visa_required INTEGER DEFAULT 0,
            vaccination_required INTEGER DEFAULT 0
        )
    ''')

    # Таблица отелей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            meal_type TEXT,
            stars INTEGER
        )
    ''')

    # Таблица туров
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tours (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country TEXT NOT NULL,
            city TEXT,
            start_date TEXT,
            end_date TEXT,
            price REAL,
            hotel_id INTEGER,
            FOREIGN KEY (hotel_id) REFERENCES hotels(id)
        )
    ''')

    # Таблица бронирований
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            tour_id INTEGER,
            status TEXT,
            booking_date TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id),
            FOREIGN KEY (tour_id) REFERENCES tours(id)
        )
    ''')

    # Таблица авиабилетов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER,
            flight_number TEXT,
            departure_airport TEXT,
            arrival_airport TEXT,
            departure_date TEXT,
            arrival_date TEXT,
            FOREIGN KEY (booking_id) REFERENCES bookings(id)
        )
    ''')

    # Таблица гидов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            language TEXT,
            phone TEXT
        )
    ''')

    # Таблица договоров
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER,
            file_url TEXT,
            date TEXT,
            FOREIGN KEY (booking_id) REFERENCES bookings(id)
        )
    ''')

    # Таблица трансферов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transfers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tour_id INTEGER,
            transfer_date TEXT,
            location TEXT,
            FOREIGN KEY (tour_id) REFERENCES tours(id)
        )
    ''')

    clients = [
        ("Иван Иванов", "1234567890", "+79991234567", "ivan@example.com", "Пляжный отдых", 1, 0),
        ("Мария Петрова", "9876543210", "+79997654321", "maria@example.com", "Экскурсии", 0, 1),
        ("Алексей Смирнов", "1112223334", "+79990001122", "alex@example.com", "Активный отдых", 0, 0),
    ]
    cursor.executemany('''
            INSERT INTO clients (full_name, passport, phone, email, preferences, visa_required, vaccination_required)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', clients)

    hotels = [
        ("Отель Москва", "Москва, ул. Красная, 1", "Завтрак", 4),
        ("Отель Сочи", "Сочи, ул. Морская, 10", "Полупансион", 5),
    ]
    cursor.executemany('''
            INSERT INTO hotels (name, address, meal_type, stars)
            VALUES (?, ?, ?, ?)
        ''', hotels)

    tours = [
        ("Россия", "Москва", "2025-07-01", "2025-07-10", 50000.0, 1),
        ("Россия", "Сочи", "2025-08-05", "2025-08-15", 75000.0, 2),
    ]
    cursor.executemany('''
            INSERT INTO tours (country, city, start_date, end_date, price, hotel_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', tours)

    bookings = [
        (1, 1, "Подтверждена", datetime.now().strftime("%Y-%m-%d")),
        (2, 2, "Ожидает оплаты", datetime.now().strftime("%Y-%m-%d")),
    ]
    cursor.executemany('''
            INSERT INTO bookings (client_id, tour_id, status, booking_date)
            VALUES (?, ?, ?, ?)
        ''', bookings)

    conn.commit()
    conn.close()
    print("✅ Таблицы успешно созданы.")

if __name__ == '__main__':
    create_tables()
