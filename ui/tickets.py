import tkinter as tk
from tkinter import ttk, messagebox
from database.database.connection import get_connection


class TicketManager(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.load_tickets()

    def create_widgets(self):
        columns = ("id", "booking_id", "flight_number", "departure_airport", "arrival_airport", "departure_date", "arrival_date")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.replace('_', ' ').capitalize())
            self.tree.column(col, anchor=tk.CENTER, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True)

        form = ttk.Frame(self)
        form.pack(fill=tk.X, pady=10)

        labels = ["ID бронирования", "Номер рейса", "Аэропорт вылета", "Аэропорт прилёта", "Дата вылета", "Дата прилёта"]
        self.entries = {}
        for i, label in enumerate(labels):
            ttk.Label(form, text=label).grid(row=0, column=i)
            entry = ttk.Entry(form)
            entry.grid(row=1, column=i, padx=5)
            self.entries[label] = entry

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="Добавить", command=self.add_ticket).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self.delete_ticket).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Обновить", command=self.load_tickets).pack(side=tk.LEFT, padx=5)

    def load_tickets(self):
        self.tree.delete(*self.tree.get_children())
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT id, booking_id, flight_number, departure_airport, arrival_airport, departure_date, arrival_date FROM tickets""")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()

    def add_ticket(self):
        try:
            booking_id = int(self.entries["ID бронирования"].get())
            flight_number = self.entries["Номер рейса"].get().strip()
            departure_airport = self.entries["Аэропорт вылета"].get().strip()
            arrival_airport = self.entries["Аэропорт прилёта"].get().strip()
            departure_date = self.entries["Дата вылета"].get().strip()
            arrival_date = self.entries["Дата прилёта"].get().strip()
            if not flight_number:
                raise ValueError("Номер рейса обязателен")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tickets (booking_id, flight_number, departure_airport, arrival_airport, departure_date, arrival_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (booking_id, flight_number, departure_airport, arrival_airport, departure_date, arrival_date))
        conn.commit()
        conn.close()
        self.load_tickets()
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def delete_ticket(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления")
            return
        ticket_id = self.tree.item(selected[0])['values'][0]
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
        conn.commit()
        conn.close()
        self.load_tickets()
