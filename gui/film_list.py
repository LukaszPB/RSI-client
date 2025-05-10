import tkinter as tk
from soap_comunication import *
from PIL import Image, ImageTk  # użyj Pillow do skalowania zdjęć

class FilmList(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        header = tk.Label(self, text="Lista filmów", font=("Helvetica", 16, "bold"))
        header.pack(pady=20)

        film_container = tk.Frame(self)
        film_container.pack(pady=10)

        films = getMovies()

        row_num = 0
        col_num = 0

        for film in films:
            film_frame = tk.Frame(film_container, bd=1, relief="solid", padx=10, pady=10)
            film_frame.grid(row=row_num, column=col_num, padx=10, pady=10, sticky="n")

            # Załaduj i przeskaluj obraz
            if film['image']:  # jeśli ścieżka istnieje
                try:
                    img = Image.open(film['image'])
                except:
                    img = Image.open("gui/okladka.png")  # fallback
            else:
                img = Image.open("gui/okladka.png")

            img = img.resize((64, 96))  # zmniejsz obraz
            photo = ImageTk.PhotoImage(img)

            image_label = tk.Label(film_frame, image=photo)
            image_label.image = photo
            image_label.grid(row=0, column=0, rowspan=6, padx=5)

            # Dane filmu obok obrazu
            tk.Label(film_frame, text=film['title'], font=("Helvetica", 12, "bold")).grid(row=0, column=1, sticky="w")
            tk.Label(film_frame, text=f"Reżyser: {film['director']}").grid(row=1, column=1, sticky="w")
            tk.Label(film_frame, text=f"Data wydania: {film['releaseDate']}").grid(row=2, column=1, sticky="w")
            tk.Label(film_frame, text=f"Typ filmu: {film['movieType']}").grid(row=3, column=1, sticky="w")
            tk.Label(film_frame, text="Opis: " + film['description']).grid(row=4, column=1, sticky="w")
            if film['actorList']:
                tk.Label(film_frame, text="Aktorzy: " + ", ".join(film['actorList'])).grid(row=5, column=1, sticky="w")
            else:
                tk.Label(film_frame, text="Brak aktorów w obsadzie").grid(row=5, column=1, sticky="w")

            # Przycisk Rezerwuj
            reserve_button = tk.Button(
                film_frame, text="Rezerwuj", bg="green", fg="white",
                command=lambda f=film: controller.show_page("ReservationMaking", f['title'])
            )
            reserve_button.grid(row=6, column=1, pady=5, sticky="e")

            # Ustawienie kolumny i rzędu
            col_num += 1
            if col_num >= 2:
                col_num = 0
                row_num += 1

        tk.Button(self, text="Lista rezerwacji",
                  command=lambda: controller.show_page("ReservationList")).pack(pady=20)