import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class BookingForm(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.conn = sqlite3.connect('travel_agency.db')
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Бронирование тура", font=("Arial", 16)).pack(pady=10)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="ID тура:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.tour_id_entry = ttk.Entry(form)
        self.tour_id_entry.grid(row=0, column=1, padx=5)

        ttk.Label(form, text="Имя клиента:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.client_name_entry = ttk.Entry(form)
        self.client_name_entry.grid(row=1, column=1, padx=5)

        ttk.Label(form, text="Email клиента:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.client_email_entry = ttk.Entry(form)
        self.client_email_entry.grid(row=2, column=1, padx=5)

        ttk.Label(form, text="Дата бронирования:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.date_entry = ttk.Entry(form)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=3, column=1, padx=5)

        ttk.Button(self, text="Забронировать", command=self.save_booking).pack(pady=15)

    def save_booking(self):
        tour_id = self.tour_id_entry.get().strip()
        name = self.client_name_entry.get().strip()
        email = self.client_email_entry.get().strip()
        date = self.date_entry.get().strip()

        if not (tour_id and name and email and date):
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            cursor = self.conn.cursor()

            # 1. Создать клиента, если его нет
            cursor.execute("SELECT id FROM clients WHERE name=? AND email=?", (name, email))
            client = cursor.fetchone()
            if client:
                client_id = client[0]
            else:
                cursor.execute("INSERT INTO clients (name, email) VALUES (?, ?)", (name, email))
                client_id = cursor.lastrowid

            # 2. Создать бронь
            cursor.execute("""
                INSERT INTO bookings (client_id, tour_id, booking_date)
                VALUES (?, ?, ?)
            """, (client_id, tour_id, date))

            self.conn.commit()
            messagebox.showinfo("Успех", f"Бронирование создано. Ваучер №{cursor.lastrowid}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при бронировании: {e}")
