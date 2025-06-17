import tkinter as tk
from tkinter import ttk
from ui import tour_search, booking, clients, logistics  # ✅ добавлен logistics


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Travel Agency System")
        self.geometry("900x600")

        # Главное меню
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Меню "Туры"
        tour_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Туры", menu=tour_menu)
        tour_menu.add_command(label="Поиск туров", command=self.open_tour_search)

        # Меню "Бронирование"
        booking_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Бронирование", menu=booking_menu)
        booking_menu.add_command(label="Создать бронь", command=self.open_booking)

        # Меню "Клиенты"
        client_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Клиенты", menu=client_menu)
        client_menu.add_command(label="Управление клиентами", command=self.open_clients)

        # ✅ Меню "Логистика"
        logistics_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Логистика", menu=logistics_menu)
        logistics_menu.add_command(label="Управление логистикой", command=self.open_logistics)

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def open_tour_search(self):
        self.clear_frame()
        tour_search.TourSearch(self.main_frame).pack(fill=tk.BOTH, expand=True)

    def open_booking(self):
        self.clear_frame()
        booking.BookingForm(self.main_frame).pack(fill=tk.BOTH, expand=True)

    def open_clients(self):
        self.clear_frame()
        clients.ClientManager(self.main_frame).pack(fill=tk.BOTH, expand=True)

    # ✅ Метод для логистики
    def open_logistics(self):
        self.clear_frame()
        logistics.LogisticsManager(self.main_frame).pack(fill=tk.BOTH, expand=True)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
