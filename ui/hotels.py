import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class HotelManager(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.conn = sqlite3.connect('travel_agency.db')
        self.create_widgets()
        self.load_hotels()

    def create_widgets(self):
        # Таблица
        columns = ("id", "name", "address", "meal_type", "stars")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor=tk.CENTER, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Форма ввода
        form = ttk.Frame(self)
        form.pack(fill=tk.X, pady=10)

        labels = ["Название", "Адрес", "Тип питания", "Звёзды"]
        self.entries = {}
        for i, text in enumerate(labels):
            ttk.Label(form, text=text).grid(row=0, column=i)
            entry = ttk.Entry(form)
            entry.grid(row=1, column=i, padx=5)
            self.entries[text] = entry

        # Кнопки
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="Добавить", command=self.add_hotel).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self.delete_hotel).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Обновить", command=self.load_hotels).pack(side=tk.LEFT, padx=5)

    def load_hotels(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, address, meal_type, stars FROM hotels")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

    def add_hotel(self):
        try:
            name = self.entries["Название"].get()
            address = self.entries["Адрес"].get()
            meal_type = self.entries["Тип питания"].get()
            stars = int(self.entries["Звёзды"].get())
            if not name:
                raise ValueError("Название обязательно")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            return

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO hotels (name, address, meal_type, stars) VALUES (?, ?, ?, ?)",
                       (name, address, meal_type, stars))
        self.conn.commit()
        self.load_hotels()
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def delete_hotel(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления")
            return
        item = self.tree.item(selected[0])
        hotel_id = item['values'][0]
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM hotels WHERE id = ?", (hotel_id,))
        self.conn.commit()
        self.load_hotels()
