import tkinter as tk
from soap_comunication import *

class ReservationList(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        header = tk.Label(self, text="Lista rezerwacji:", font=("Helvetica", 16))
        header.pack(pady=10)

        self.film_container = tk.Frame(self)
        self.film_container.pack(pady=5)

        # Dwa przyciski obok siebie na dole
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Lista seansów",
                  command=lambda: controller.show_page("ShowingList")).pack(side="left", padx=10)

        tk.Button(button_frame, text="Lista filmów",
                  command=lambda: controller.show_page("FilmList")).pack(side="left", padx=10)

        
    def set_data(self, value = ""):
        self.reservations = getReservations()  # Zakładam, że to lista słowników z danymi filmów)
        self.set_up()

    def set_up(self):
        for widget in self.film_container.winfo_children():
            widget.destroy()

        for row_num, reservation in enumerate(self.reservations):
            film_frame = tk.Frame(self.film_container, bd=1, padx=10, pady=5)
            film_frame.grid(row=row_num, column=0, padx=5, pady=3, sticky="w")

            reservation_id = reservation['reservationId']
            showing_id = reservation['showingId']
            seats = reservation['seatLocationList']['seatLocation']
            seat_str = ', '.join(f"({seat['x']}, {seat['y']})" for seat in seats)

            text = f"Rezerwacja #{reservation_id} | Seans ID: {showing_id} | Miejsca: {seat_str}"

            tk.Label(film_frame, text=text, font=("Helvetica", 11), anchor="w", justify="left").grid(row=0, column=0, sticky="w")

            edit_button = tk.Button(
                film_frame, text="Edytuj", bg="lightblue", fg="black",
                command=lambda res_id=reservation_id: self.update(res_id)
            )
            edit_button.grid(row=0, column=1, padx=5)

            delete_button = tk.Button(
                film_frame, text="Usuń", bg="red", fg="white",
                command=lambda res_id=reservation_id: self.delete(res_id)
            )
            delete_button.grid(row=0, column=2, padx=5)

            pdf_downland_button = tk.Button(
                film_frame, text="Pobierz PDF", bg="lightgrey", fg="white",
                command=lambda res_id=reservation_id: getPDF(res_id)
            )
            pdf_downland_button.grid(row=0, column=3, padx=5)

    def delete(self, id):
        deleteReservations(id)
        self.reservations = getReservations()
        self.set_up()

    def update(self,reservation):
        self.controller.show_page("ReservationUpdating", getReservation(reservation))
        self.reservations = getReservations()
        self.set_up()