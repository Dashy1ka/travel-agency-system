import tkinter as tk
from tkinter import ttk, messagebox
from database.database.connection import get_connection


class LogisticsManager(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.load_guides()
        self.load_tours()
        self.load_transfers()

    def create_widgets(self):
        ttk.Label(self, text="Управление логистикой", font=("Arial", 16)).pack(pady=10)

        # Гиды
        guides_frame = ttk.LabelFrame(self, text="Гиды")
        guides_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.guides_tree = ttk.Treeview(guides_frame, columns=("Name", "Language", "Phone"), show="headings")
        for col in ("Name", "Language", "Phone"):
            self.guides_tree.heading(col, text=col)
            self.guides_tree.column(col, width=120)
        self.guides_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(guides_frame, orient=tk.VERTICAL, command=self.guides_tree.yview)
        self.guides_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Button(guides_frame, text="Добавить гида", command=self.add_guide_popup).pack(pady=5)

        # Трансферы
        transfers_frame = ttk.LabelFrame(self, text="Трансферы")
        transfers_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.transfers_tree = ttk.Treeview(transfers_frame, columns=("Tour", "Date", "Location"), show="headings")
        for col in ("Tour", "Date", "Location"):
            self.transfers_tree.heading(col, text=col)
            self.transfers_tree.column(col, width=150)
        self.transfers_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar2 = ttk.Scrollbar(transfers_frame, orient=tk.VERTICAL, command=self.transfers_tree.yview)
        self.transfers_tree.configure(yscroll=scrollbar2.set)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Button(transfers_frame, text="Добавить трансфер", command=self.add_transfer_popup).pack(pady=5)

    def load_guides(self):
        self.guides_tree.delete(*self.guides_tree.get_children())
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, language, phone FROM guides")
        for gid, name, lang, phone in cursor.fetchall():
            self.guides_tree.insert("", "end", iid=gid, values=(name, lang, phone))
        conn.close()

    def load_tours(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, country, city, start_date, end_date FROM tours")
        self.tours = {
            f"{row[1]}, {row[2]} ({row[3]} - {row[4]}) (ID:{row[0]})": row[0]
            for row in cursor.fetchall()
        }
        conn.close()

    def load_transfers(self):
        self.transfers_tree.delete(*self.transfers_tree.get_children())
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT transfers.id, tours.country, tours.city, transfers.transfer_date, transfers.location
            FROM transfers 
            LEFT JOIN tours ON transfers.tour_id = tours.id
        """)
        for tid, country, city, date, location in cursor.fetchall():
            tour_str = f"{country}, {city}"
            self.transfers_tree.insert("", "end", iid=tid, values=(tour_str, date, location))
        conn.close()

    def add_guide_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Добавить гида")

        ttk.Label(popup, text="Имя:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(popup)
        name_entry.grid(row=0, column=1)

        ttk.Label(popup, text="Язык:").grid(row=1, column=0, padx=5, pady=5)
        lang_entry = ttk.Entry(popup)
        lang_entry.grid(row=1, column=1)

        ttk.Label(popup, text="Телефон:").grid(row=2, column=0, padx=5, pady=5)
        phone_entry = ttk.Entry(popup)
        phone_entry.grid(row=2, column=1)

        def add_guide():
            name = name_entry.get().strip()
            lang = lang_entry.get().strip()
            phone = phone_entry.get().strip()
            if not name:
                messagebox.showerror("Ошибка", "Имя обязательно")
                return
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO guides (name, language, phone) VALUES (?, ?, ?)", (name, lang, phone))
            conn.commit()
            conn.close()
            self.load_guides()
            popup.destroy()

        ttk.Button(popup, text="Добавить", command=add_guide).grid(row=3, column=0, columnspan=2, pady=10)

    def add_transfer_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Добавить трансфер")

        ttk.Label(popup, text="Тур:").grid(row=0, column=0, padx=5, pady=5)
        tour_cb = ttk.Combobox(popup, state="readonly")
        tour_cb.grid(row=0, column=1)
        tour_cb['values'] = list(self.tours.keys())
        if self.tours:
            tour_cb.current(0)

        ttk.Label(popup, text="Дата трансфера:").grid(row=1, column=0, padx=5, pady=5)
        date_entry = ttk.Entry(popup)
        date_entry.grid(row=1, column=1)

        ttk.Label(popup, text="Локация:").grid(row=2, column=0, padx=5, pady=5)
        location_entry = ttk.Entry(popup)
        location_entry.grid(row=2, column=1)

        def add_transfer():
            tour_text = tour_cb.get()
            transfer_date = date_entry.get().strip()
            location = location_entry.get().strip()
            if not tour_text or not transfer_date or not location:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            tour_id = self.tours[tour_text]
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO transfers (tour_id, transfer_date, location) VALUES (?, ?, ?)",
                (tour_id, transfer_date, location)
            )
            conn.commit()
            conn.close()
            self.load_transfers()
            popup.destroy()

        ttk.Button(popup, text="Добавить", command=add_transfer).grid(row=3, column=0, columnspan=2, pady=10)
