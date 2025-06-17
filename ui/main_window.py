import tkinter as tk
from tkinter import ttk
import time
from ui import tour_search, booking, clients, logistics, hotels, tickets  # Добавил hotels и tickets


class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("400x200")
        self.overrideredirect(True)
        self.configure(bg="#f0f0f0")

        self.label = tk.Label(self, text="Travel Agency System", font=("Segoe UI", 24, "bold"), fg="#c00", bg="#f0f0f0")
        self.label.pack(expand=True)

        self.progress = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=300)
        self.progress.pack(pady=20)
        self.progress['maximum'] = 100
        self.after(50, self.load)

    def load(self):
        current = self.progress['value']
        if current < 100:
            self.progress['value'] = current + 5
            self.after(100, self.load)
        else:
            self.destroy()


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Travel Agency System")
        self.geometry("900x600")
        self.configure(bg="#f7f7f7")

        # Заголовок
        title = tk.Label(self, text="Travel Agency System", font=("Segoe UI", 32, "bold"), fg="#c00", bg="#f7f7f7")
        title.pack(pady=40)

        # Крупные кнопки в центре
        btn_frame = tk.Frame(self, bg="#f7f7f7")
        btn_frame.pack(expand=True)

        btn_style = {"font": ("Segoe UI", 16, "bold"), "width": 20, "height": 2, "bg": "#e0e0e0", "fg": "#c00",
                     "activebackground": "#ff4d4d", "relief": "raised", "bd": 3}

        self.btn_tours = tk.Button(btn_frame, text="Поиск туров", command=self.open_tour_search, **btn_style)
        self.btn_booking = tk.Button(btn_frame, text="Создать бронь", command=self.open_booking, **btn_style)
        self.btn_clients = tk.Button(btn_frame, text="Управление клиентами", command=self.open_clients, **btn_style)
        self.btn_logistics = tk.Button(btn_frame, text="Трансферы и гиды", command=self.open_logistics, **btn_style)
        self.btn_hotels = tk.Button(btn_frame, text="Управление отелями", command=self.open_hotels, **btn_style)
        self.btn_tickets = tk.Button(btn_frame, text="Управление билетами", command=self.open_tickets, **btn_style)

        self.btn_tours.grid(row=0, column=0, padx=20, pady=10)
        self.btn_booking.grid(row=0, column=1, padx=20, pady=10)
        self.btn_clients.grid(row=1, column=0, padx=20, pady=10)
        self.btn_logistics.grid(row=1, column=1, padx=20, pady=10)
        self.btn_hotels.grid(row=2, column=0, padx=20, pady=10)
        self.btn_tickets.grid(row=2, column=1, padx=20, pady=10)

        # Основной фрейм под динамический контент
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def open_tour_search(self):
        self.clear_frame()
        tour_search.TourSearch(self.main_frame).pack(fill=tk.BOTH, expand=True)

    def open_booking(self):
        self.clear_frame()
        booking.BookingForm(self.main_frame).pack(fill=tk.BOTH, expand=True)

    def open_clients(self):
        self.clear_frame()
        clients.ClientManager(self.main_frame).pack(fill=tk.BOTH, expand=True)

    def open_logistics(self):
        self.clear_frame()
        logistics.LogisticsManager(self.main_frame).pack(fill=tk.BOTH, expand=True)

    def open_hotels(self):
        self.clear_frame()
        hotels.HotelManager(self.main_frame).pack(fill=tk.BOTH, expand=True)

    def open_tickets(self):
        self.clear_frame()
        tickets.TicketManager(self.main_frame).pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = MainWindow()
    splash = SplashScreen(root)
    root.withdraw()  # Скрываем главное окно

    def show_main():
        splash.destroy()
        root.deiconify()

    # Показываем сплеш на 3 секунды (примерно, зависит от прогрессбара)
    splash.after(3200, show_main)
    root.mainloop()
