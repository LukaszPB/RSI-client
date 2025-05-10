import tkinter as tk
class ReservationList(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Lista rezerwacji").pack(pady=10)
        tk.Button(self, text="Zamówienie",
                  command=lambda: controller.show_page("ReservationMaking")).pack()
        tk.Button(self, text="Lista filmów",
                  command=lambda: controller.show_page("FilmList")).pack()