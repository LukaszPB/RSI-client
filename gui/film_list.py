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
            film_frame = tk.Frame(film_container, bd=1, padx=50, pady=10)
            film_frame.grid(row=row_num, column=col_num, padx=10, pady=10, sticky="n")
      
            # Załaduj i przeskaluj obraz
            if film['image']:  # jeśli ścieżka istnieje
                try:
                    img_data = getImage(film['image'])
        
                    # Otwórz obraz z danych binarnych
                    img = Image.open(BytesIO(img_data))  # otwieramy obraz z binarnych danych
                except:
                    img = Image.open("gui/okladka.png")  # fallback
            else:
                img = Image.open("gui/okladka.png")

            img = img.resize((100, 150))  # zmniejsz obraz
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
            actors = "Aktorzy: "
            for id in film['actorIdList']['actorId']:
                actor = getActor(id)
                actors += actor['firstName'] + " " + actor['lastName'] + ", "
            tk.Label(film_frame, text=actors, wraplength=200, justify="left").grid(row=5, column=1, sticky="w")

            # Ustawienie kolumny i rzędu
            col_num += 1
            if col_num >= 3:
                col_num = 0
                row_num += 2

        # tk.Button(self, text="Lista rezerwacji",
        #           command=lambda: controller.show_page("ReservationList")).pack(pady=20)
        # Dwa przyciski obok siebie na dole
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Lista seansów",
                  command=lambda: controller.show_page("ShowingList")).pack(side="left", padx=10)

        tk.Button(button_frame, text="Lista rezerwacji",
                  command=lambda: controller.show_page("ReservationList")).pack(side="left", padx=10)