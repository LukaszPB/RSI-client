import tkinter as tk
from soap_comunication import *
from PIL import Image, ImageTk  # użyj Pillow do skalowania zdjęć

class ShowingList(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        header = tk.Label(self, text="Seansy:", font=("Helvetica", 16))
        header.pack(pady=10)

        film_container = tk.Frame(self)
        film_container.pack(pady=5)

        films = getShowings()  # Zakładam, że to lista słowników z danymi filmów

        for row_num, film in enumerate(films):
            film_frame = tk.Frame(film_container, bd=1, padx=10, pady=5)
            film_frame.grid(row=row_num, column=0, padx=5, pady=3, sticky="w")

            # Wszystko w jednej linii (jeden rząd, wiele kolumn)
            tk.Label(film_frame, text='Seans ID: ' + str(film['movie']['id']), font=("Helvetica", 12)).grid(row=0, column=0, padx=5, sticky="w")
            tk.Label(film_frame, text=film['movie']['title'], font=("Helvetica", 12)).grid(row=0, column=1, padx=5, sticky="w")
            tk.Label(film_frame, text=film['showingDateAndTime'], font=("Helvetica", 12)).grid(row=0, column=2, padx=5, sticky="w")

            reserve_button = tk.Button(
                film_frame, text="Rezerwuj", bg="green", fg="white",
                command=lambda f=film: controller.show_page("ReservationMaking", f)
            )
            reserve_button.grid(row=0, column=3, padx=10, sticky="e")

        # Dwa przyciski obok siebie na dole
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Lista filmów",
                  command=lambda: controller.show_page("FilmList")).pack(side="left", padx=10)

        tk.Button(button_frame, text="Lista rezerwacji",
                  command=lambda: controller.show_page("ReservationList")).pack(side="left", padx=10)