import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

class TourSearch(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.conn = sqlite3.connect('travel_agency.db')
        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        ttk.Label(self, text="Поиск туров", font=("Arial", 16)).pack(pady=10)

        # Фильтры
        filters_frame = ttk.Frame(self)
        filters_frame.pack(pady=10, fill=tk.X)

        ttk.Label(filters_frame, text="Страна:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.country_entry = ttk.Entry(filters_frame)
        self.country_entry.grid(row=0, column=1, padx=5)

        ttk.Label(filters_frame, text="Дата с (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.date_from_entry = ttk.Entry(filters_frame)
        self.date_from_entry.grid(row=1, column=1, padx=5)

        ttk.Label(filters_frame, text="Дата по (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.date_to_entry = ttk.Entry(filters_frame)
        self.date_to_entry.grid(row=2, column=1, padx=5)

        ttk.Label(filters_frame, text="Максимальная цена:").grid(row=3, column=0, sticky=tk.W, padx=5)
        self.price_entry = ttk.Entry(filters_frame)
        self.price_entry.grid(row=3, column=1, padx=5)

        # Кнопка поиска
        ttk.Button(self, text="Искать", command=self.search_tours).pack(pady=10)

        # Результаты
        self.tree = ttk.Treeview(self, columns=("country", "city", "start_date", "end_date", "price", "hotel"), show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)

        for col in ("country", "city", "start_date", "end_date", "price", "hotel"):
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100)

    def search_tours(self):
        country = self.country_entry.get().strip()
        date_from = self.date_from_entry.get().strip()
        date_to = self.date_to_entry.get().strip()
        price = self.price_entry.get().strip()

        query = """
            SELECT t.id, t.country, t.city, t.start_date, t.end_date, t.price, h.name
            FROM tours t
            LEFT JOIN hotels h ON t.hotel_id = h.id
            WHERE 1=1
        """
        params = []

        if country:
            query += " AND t.country LIKE ?"
            params.append(f"%{country}%")

        if date_from:
            try:
                datetime.strptime(date_from, "%Y-%m-%d")
                query += " AND t.start_date >= ?"
                params.append(date_from)
            except ValueError:
                pass  # Можно показать ошибку позже

        if date_to:
            try:
                datetime.strptime(date_to, "%Y-%m-%d")
                query += " AND t.end_date <= ?"
                params.append(date_to)
            except ValueError:
                pass

        if price:
            try:
                price_val = float(price)
                query += " AND t.price <= ?"
                params.append(price_val)
            except ValueError:
                pass

        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Очистить предыдущие результаты
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in rows:
            # row: id, country, city, start_date, end_date, price, hotel_name
            self.tree.insert('', 'end', values=row[1:])

