import tkinter as tk
from tkinter import ttk
from database.database.connection import get_connection  # импортируем get_connection

class TourSearch(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_widgets()
        self.populate_results([])

    def create_widgets(self):
        form_frame = ttk.Frame(self)
        form_frame.pack(fill=tk.X, pady=10)

        ttk.Label(form_frame, text="Страна:").grid(row=0, column=0, padx=5, pady=5)
        self.country_entry = ttk.Entry(form_frame)
        self.country_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Дата начала (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5)
        self.start_date_entry = ttk.Entry(form_frame)
        self.start_date_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Дата конца (YYYY-MM-DD):").grid(row=0, column=4, padx=5, pady=5)
        self.end_date_entry = ttk.Entry(form_frame)
        self.end_date_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(form_frame, text="Максимальная цена:").grid(row=0, column=6, padx=5, pady=5)
        self.max_price_entry = ttk.Entry(form_frame)
        self.max_price_entry.grid(row=0, column=7, padx=5, pady=5)

        search_btn = ttk.Button(form_frame, text="Поиск", command=self.search_tours)
        search_btn.grid(row=0, column=8, padx=5, pady=5)

        # Таблица результатов
        self.tree = ttk.Treeview(self, columns=("country", "city", "start_date", "end_date", "price"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor=tk.CENTER, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def search_tours(self):
        country = self.country_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        max_price = self.max_price_entry.get()

        query = "SELECT country, city, start_date, end_date, price FROM tours WHERE 1=1"
        params = []

        if country:
            query += " AND country LIKE ?"
            params.append(f"%{country}%")
        if start_date:
            query += " AND start_date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND end_date <= ?"
            params.append(end_date)
        if max_price:
            try:
                price_val = float(max_price)
                query += " AND price <= ?"
                params.append(price_val)
            except ValueError:
                pass  # Игнорируем неправильный ввод цены

        conn = get_connection()  # используем get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        self.populate_results(results)

    def populate_results(self, tours):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for tour in tours:
            self.tree.insert("", "end", values=tour)
