import tkinter as tk
from gui.film_list import *
from gui.reservation_list import *
from gui.reservation_making import *
from gui.reservation_updating import *
from gui.showing_list import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wielowidokowa aplikacja")
        self.geometry("1200x700")
        self.pages = {}

        for Ekran in (ReservationUpdating, FilmList, ReservationList, ReservationMaking,ShowingList):
            name = Ekran.__name__
            frame = Ekran(self, self)
            self.pages[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_page("ShowingList")

    def show_page(self, page_name, value = None):
        frame = self.pages[page_name]
        if hasattr(frame, "set_data"):
            frame.set_data(value)
        frame.tkraise()