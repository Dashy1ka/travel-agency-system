import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class BookingForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.conn = sqlite3.connect('travel_agency.db')
        self.create_widgets()
        self.load_clients()
        self.load_tours()

    def create_widgets(self):
        ttk.Label(self, text="Создать бронирование", font=("Arial", 16)).pack(pady=10)

        frame = ttk.Frame(self)
        frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Label(frame, text="Клиент:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.client_cb = ttk.Combobox(frame, state="readonly")
        self.client_cb.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        ttk.Label(frame, text="Тур:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.tour_cb = ttk.Combobox(frame, state="readonly")
        self.tour_cb.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        ttk.Label(frame, text="Статус:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.status_cb = ttk.Combobox(frame, state="readonly", values=["Новая", "Подтверждена", "Отменена"])
        self.status_cb.current(0)
        self.status_cb.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)

        ttk.Button(self, text="Создать бронь", command=self.create_booking).pack(pady=10)

        frame.columnconfigure(1, weight=1)

    def load_clients(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, full_name FROM clients")
        rows = cursor.fetchall()
        self.clients = {f"{row[1]} (ID:{row[0]})": row[0] for row in rows}
        self.client_cb['values'] = list(self.clients.keys())
        if rows:
            self.client_cb.current(0)

    def load_tours(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, country, city, start_date, end_date FROM tours")
        rows = cursor.fetchall()
        self.tours = {f"{row[1]}, {row[2]} с {row[3]} по {row[4]} (ID:{row[0]})": row[0] for row in rows}
        self.tour_cb['values'] = list(self.tours.keys())
        if rows:
            self.tour_cb.current(0)

    def create_booking(self):
        client_text = self.client_cb.get()
        tour_text = self.tour_cb.get()
        status = self.status_cb.get()

        if not client_text or not tour_text:
            messagebox.showerror("Ошибка", "Выберите клиента и тур")
            return

        client_id = self.clients[client_text]
        tour_id = self.tours[tour_text]
        booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO bookings (client_id, tour_id, status, booking_date) VALUES (?, ?, ?, ?)",
            (client_id, tour_id, status, booking_date)
        )
        self.conn.commit()
        messagebox.showinfo("Успех", "Бронирование успешно создано")

        # обновим поля
        self.load_clients()
        self.load_tours()
