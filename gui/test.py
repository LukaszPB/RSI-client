import tkinter as tk
import os

root = tk.Tk()
print("Aktualny katalog roboczy:", os.getcwd())

img = tk.PhotoImage(file="gui/okladka.png")  # plik PNG w tym samym folderze
label = tk.Label(root, image=img)
label.image = img  # ZACHOWANIE REFERENCJI
label.pack()

root.mainloop()