import tkinter as tk

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Zaloguj się", font=("Helvetica", 16, "bold")).pack(pady=20)

        # Pole loginu
        tk.Label(self, text="Login:").pack()
        self.login_entry = tk.Entry(self)
        self.login_entry.pack(pady=5)

        # Pole hasła (opcjonalnie)
        tk.Label(self, text="Hasło:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        # Przycisk logowania
        tk.Button(self, text="Zaloguj",
                  command=self.login).pack(pady=10)

    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        # Można dodać prostą walidację
        if login == "admin" and password == "1234":
            print(f"Zalogowano jako: {login}")
            self.controller.show_page("FilmList", value=login)
        else:
            tk.Label(self, text="Błędny login lub hasło", fg="red").pack()