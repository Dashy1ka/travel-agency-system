import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class ClientManager(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.conn = sqlite3.connect('travel_agency.db')
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Клиенты", font=("Arial", 16)).pack(pady=10)

        # Таблица
        self.tree = ttk.Treeview(self, columns=("id", "name", "email", "preferences", "visa_required", "vaccination_required"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.replace("_", " ").capitalize())

        self.tree.bind("<Double-1>", self.on_row_select)

        # Форма редактирования
        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Аллергии/Питание:").grid(row=0, column=0, padx=5, pady=5)
        self.pref_entry = ttk.Entry(form, width=40)
        self.pref_entry.grid(row=0, column=1, padx=5)

        self.visa_var = tk.IntVar()
        ttk.Checkbutton(form, text="Требуется виза", variable=self.visa_var).grid(row=1, column=0, columnspan=2, sticky=tk.W)

        self.vacc_var = tk.IntVar()
        ttk.Checkbutton(form, text="Требуются прививки", variable=self.vacc_var).grid(row=2, column=0, columnspan=2, sticky=tk.W)

        ttk.Button(self, text="Сохранить изменения", command=self.save_preferences).pack(pady=10)

        self.load_clients()

    def load_clients(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, email, preferences, visa_required, vaccination_required FROM clients")
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)

    def on_row_select(self, event):
        selected = self.tree.item(self.tree.selection())["values"]
        if not selected:
            return
        self.selected_client_id = selected[0]
        self.pref_entry.delete(0, tk.END)
        self.pref_entry.insert(0, selected[3] or "")
        self.visa_var.set(selected[4])
        self.vacc_var.set(selected[5])

    def save_preferences(self):
        if not hasattr(self, 'selected_client_id'):
            messagebox.showwarning("Внимание", "Выберите клиента из таблицы.")
            return

        prefs = self.pref_entry.get().strip()
        visa = self.visa_var.get()
        vacc = self.vacc_var.get()

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE clients
                SET preferences = ?, visa_required = ?, vaccination_required = ?
                WHERE id = ?
            """, (prefs, visa, vacc, self.selected_client_id))
            self.conn.commit()
            messagebox.showinfo("Успех", "Предпочтения клиента обновлены.")
            self.load_clients()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении: {e}")
