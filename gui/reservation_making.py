import tkinter as tk
class ReservationMaking(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.movie_name = ""
        
        # Tworzymy etykietę i przypisujemy ją do atrybutu self.label
        self.label = tk.Label(self, text="Rezerwacja " + self.movie_name)
        self.label.pack(pady=10)

        # Przycisk do przejścia do Listy filmów
        tk.Button(self, text="Lista filmów",
                  command=lambda: controller.show_page("FilmList")).pack()

        # Przycisk do przejścia do Listy rezerwacji
        tk.Button(self, text="Lista rezerwacji",
                  command=lambda: controller.show_page("ReservationList")).pack()

    # Metoda set_data, która jest odpowiedzialna za aktualizowanie tekstu etykiety
    def set_data(self, value):
        self.movie_name = value
        self.label.config(text=f"Rezerwujesz: {self.movie_name}")
