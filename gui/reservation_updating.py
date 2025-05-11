import tkinter as tk
from soap_comunication import *
from PIL import Image, ImageTk  # użyj Pillow do skalowania zdjęć

class ReservationUpdating(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.showing = None

        # Etykieta
        self.label = tk.Label(self, text="Rezerwacja ", font=("Helvetica", 14, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Dane filmu
        self.film_frame = tk.Frame(self, bd=1, padx=50, pady=10)
        self.film_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="n")

        self.grid_frame = tk.Frame(self)
        self.grid_frame.grid(row=2, column=0, columnspan=2, pady=10)

        rows = 10
        cols = 10
        self.seat_buttons = [[None for _ in range(10)] for _ in range(10)]

        # Oznaczenia kolumn A-J
        for col in range(cols):
            label = tk.Label(self.grid_frame, text=chr(65 + col), width=2)
            label.grid(row=0, column=col + 1)

        self.selected_seats = []  # przechowuje listy [row, col]
        self.selected_seats.clear()  # wyczyść poprzedni wybór

        for row in range(rows):
            tk.Label(self.grid_frame, text=str(row + 1), width=2).grid(row=row + 1, column=0)
            for col in range(cols):
                btn = tk.Button(self.grid_frame, width=2, height=1, bg="lightgray")
                btn.grid(row=row + 1, column=col + 1, padx=1, pady=1)
                btn.config(command=lambda r=row, c=col: self.toggle_seat(r, c))
                self.seat_buttons[row][col] = btn

        # Dwa przyciski obok siebie na dole
        button_frame = tk.Frame(self)
        button_frame.grid(row=8, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="edytuj",
                  command=lambda: self.update_reservation()).grid(row=0, column=1, padx=10)

        tk.Button(button_frame, text="Lista seansów",
                  command=lambda: controller.show_page("ShowingList")).grid(row=1, column=0, padx=10)

        tk.Button(button_frame, text="Lista filmów",
                  command=lambda: controller.show_page("FilmList")).grid(row=1, column=1, padx=10)

        tk.Button(button_frame, text="Lista rezerwacji",
                  command=lambda: controller.show_page("ReservationList")).grid(row=1, column=2, padx=10)

    def set_data(self, value):
        self.selected_seats.clear()
        self.selected_seats = [[item['x'], item['y']] for item in value['seatLocationList']['seatLocation']]
        print(value)
        self.reservation_id = value.reservationId

        value = getShowing(value.showingId)

        for row in self.seat_buttons:
            for button in row:
                button.config(bg='lightgray')

        seats_raw = value['seats']
        seats = [row['item'] for row in seats_raw]

        for row in range(10):
            for col in range(10):
                if seats[row][col] > 0:
                    self.seat_buttons[row][col].config(bg="red")

        for row in self.selected_seats:
            self.seat_buttons[row[0]][row[1]].config(bg='green')
      
        self.showing = value
        self.label.config(text=f"Rezerwujesz: {self.showing['movie']['title']}")

        film = self.showing['movie']

        # Załaduj i przeskaluj obraz
        if film['image']:
            try:
                img_data = getImage(film['image'])
        
                # Otwórz obraz z danych binarnych
                img = Image.open(BytesIO(img_data))  # otwieramy obraz z binarnych danych
            except:
                img = Image.open("gui/okladka.png")
        else:
            img = Image.open("gui/okladka.png")

        img = img.resize((100, 150))
        photo = ImageTk.PhotoImage(img)

        image_label = tk.Label(self.film_frame, image=photo)
        image_label.image = photo
        image_label.grid(row=0, column=0, rowspan=6, padx=5)

        # Dane filmu obok obrazu
        tk.Label(self.film_frame, text=film['title'], font=("Helvetica", 12, "bold")).grid(row=0, column=1, sticky="w")
        tk.Label(self.film_frame, text=f"Reżyser: {film['director']}").grid(row=1, column=1, sticky="w")
        tk.Label(self.film_frame, text=f"Data wydania: {film['releaseDate']}").grid(row=2, column=1, sticky="w")
        tk.Label(self.film_frame, text=f"Typ filmu: {film['movieType']}").grid(row=3, column=1, sticky="w")
        tk.Label(self.film_frame, text="Opis: " + film['description']).grid(row=4, column=1, sticky="w")

        actors = "Aktorzy: "
        for id in film['actorIdList']['actorId']:
            actor = getActor(id)
            actors += actor['firstName'] + " " + actor['lastName'] + ", "
        tk.Label(self.film_frame, text=actors, wraplength=200, justify="left").grid(row=5, column=1, sticky="w")

    def toggle_seat(self, row, col):
        btn = self.seat_buttons[row][col]
        current_color = btn.cget("bg")

        if current_color == "red":
            return  # miejsce zajęte – nic nie rób

        if current_color == "lightgray":
            btn.config(bg="green")
            self.selected_seats.append([row, col])
        elif current_color == "green":
            btn.config(bg="lightgray")
            if [row, col] in self.selected_seats:
                self.selected_seats.remove([row, col])

        print(self.selected_seats)

    def update_reservation(self):
        response = update_reservation(
            reservation_id=self.reservation_id,
            showing_id=self.showing.showingId,
            seat_list=self.selected_seats
        )
