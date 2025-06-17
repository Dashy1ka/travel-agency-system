import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class ClientManager(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.load_clients()

    def create_widgets(self):
        # Форма для добавления клиента
        form_frame = ttk.Frame(self)
        form_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(form_frame, text="ФИО:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)

        ttk.Label(form_frame, text="Паспорт:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.passport_entry = ttk.Entry(form_frame)
        self.passport_entry.grid(row=0, column=3, sticky=tk.EW, padx=5, pady=2)

        ttk.Label(form_frame, text="Телефон:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.phone_entry = ttk.Entry(form_frame)
        self.phone_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)

        ttk.Label(form_frame, text="Email:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.email_entry = ttk.Entry(form_frame)
        self.email_entry.grid(row=1, column=3, sticky=tk.EW, padx=5, pady=2)

        ttk.Label(form_frame, text="Предпочтения:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.preferences_entry = ttk.Entry(form_frame)
        self.preferences_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=2)

        # Визы и вакцинации - чекбоксы
        self.visa_var = tk.IntVar()
        self.vaccination_var = tk.IntVar()
        ttk.Checkbutton(form_frame, text="Требуется виза", variable=self.visa_var).grid(row=2, column=2, padx=5, pady=2)
        ttk.Checkbutton(form_frame, text="Требуется вакцинация", variable=self.vaccination_var).grid(row=2, column=3, padx=5, pady=2)

        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        # Кнопка добавить
        add_btn = ttk.Button(self, text="Добавить клиента", command=self.add_client)
        add_btn.pack(pady=5)

        # Таблица клиентов
        self.tree = ttk.Treeview(self, columns=("id", "full_name", "passport", "phone", "email", "preferences", "visa", "vaccination"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=30, anchor=tk.CENTER)
        self.tree.heading("full_name", text="ФИО")
        self.tree.heading("passport", text="Паспорт")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("email", text="Email")
        self.tree.heading("preferences", text="Предпочтения")
        self.tree.heading("visa", text="Виза")
        self.tree.heading("vaccination", text="Вакцинация")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Кнопка удаления выбранного клиента
        del_btn = ttk.Button(self, text="Удалить выбранного клиента", command=self.delete_client)
        del_btn.pack(pady=5)

    def load_clients(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect('travel_agency.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, full_name, passport, phone, email, preferences, visa_required, vaccination_required FROM clients
        ''')
        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            visa = "Да" if r[6] else "Нет"
            vacc = "Да" if r[7] else "Нет"
            self.tree.insert("", tk.END, values=(r[0], r[1], r[2], r[3], r[4], r[5], visa, vacc))

    def add_client(self):
        full_name = self.name_entry.get().strip()
        passport = self.passport_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        preferences = self.preferences_entry.get().strip()
        visa = self.visa_var.get()
        vaccination = self.vaccination_var.get()

        if not full_name:
            messagebox.showwarning("Ошибка", "Введите ФИО клиента")
            return

        conn = sqlite3.connect('travel_agency.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clients (full_name, passport, phone, email, preferences, visa_required, vaccination_required)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (full_name, passport, phone, email, preferences, visa, vaccination))
        conn.commit()
        conn.close()

        messagebox.showinfo("Успех", "Клиент добавлен")
        self.clear_form()
        self.load_clients()

    def delete_client(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите клиента для удаления")
            return

        client_id = self.tree.item(selected[0])["values"][0]
        confirm = messagebox.askyesno("Подтверждение", "Удалить выбранного клиента?")
        if not confirm:
            return

        conn = sqlite3.connect('travel_agency.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
        conn.commit()
        conn.close()

        self.load_clients()

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.passport_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.preferences_entry.delete(0, tk.END)
        self.visa_var.set(0)
        self.vaccination_var.set(0)
