# import tkinter as tk
# from soap_comunication import *

# # Funkcja pobierająca dane z serwera SOAP
# def print_tekst():
#     try:
#         odpowiedz = pobierz_wiadomosc()
#         pole_tekstowe.delete("1.0", tk.END)
#         pole_tekstowe.insert(tk.END, f"Odpowiedź serwera:\n{odpowiedz}")
#     except Exception as e:
#         pole_tekstowe.insert(tk.END, f"Błąd: {e}")

# # GUI
# okno = tk.Tk()
# okno.title("SOAP i Tkinter")
# okno.geometry("400x200")

# przycisk = tk.Button(okno, text="Pobierz z SOAP", command=print_tekst)
# przycisk.pack(pady=10)

# pole_tekstowe = tk.Text(okno, height=5)
# pole_tekstowe.pack(padx=10, pady=10)

# okno.mainloop()
import tkinter as tk
from gui.interface import *

if __name__ == "__main__":
    app = App()
    app.mainloop()