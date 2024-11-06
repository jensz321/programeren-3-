# Importeer de benodigde modules voor de GUI en functionaliteit
import tkinter as tk
from tkinter import messagebox
import random

# Klasse voor het spel "Getallen raden" - Gemaakt door Bryan
class NumberGuessingGame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.create_widgets()  # Initialiseer de interfacecomponenten

    # Methode om de interfacecomponenten te creëren
    def create_widgets(self):
        # Label met instructies voor de speler
        self.label = tk.Label(self, text="Raad een getal tussen 1 en 100", font=("Arial", 24))
        self.label.pack(pady=20)

        # Invoerveld voor het getal dat de speler invoert
        self.entry = tk.Entry(self, font=("Arial", 22), width=5)
        self.entry.pack(pady=10)

        # Knop om de ingevoerde gok te controleren
        self.guess_button = tk.Button(self, text="Gok", font=("Arial", 22), command=self.check_guess)
        self.guess_button.pack(pady=10)

        # Label voor de feedback (te hoog, te laag, etc.)
        self.result_label = tk.Label(self, text="", font=("Arial", 22))
        self.result_label.pack(pady=10)

        # Start een nieuw spel
        self.new_game()

    # Methode om een nieuw spel te starten
    def new_game(self):
        self.secret_number = random.randint(1, 100)  # Genereer een geheim getal tussen 1 en 100
        self.guess_count = 0  # Reset het aantal pogingen
        self.result_label.config(text="")  # Reset het resultaatlabel

    # Methode om de gok van de speler te controleren
    def check_guess(self):
        try:
            guess = int(self.entry.get())  # Haal de invoer op en zet om naar een geheel getal
            self.guess_count += 1  # Verhoog het aantal pogingen

            # Geef feedback op basis van de gok van de speler
            if guess < self.secret_number:
                self.result_label.config(text="Te laag!")
            elif guess > self.secret_number:
                self.result_label.config(text="Te hoog!")
            else:
                # Laat zien dat het getal correct geraden is
                self.result_label.config(text=f"Goed geraden! Je deed {self.guess_count} pogingen.")
                messagebox.showinfo("Gefeliciteerd!", f"Je hebt het getal geraden in {self.guess_count} pogingen!")
                self.new_game()  # Start een nieuw spel als het getal geraden is

        except ValueError:
            # Als de invoer geen geldig getal is, toon een foutmelding
            messagebox.showerror("Fout", "Voer een geldig getal in")

# Klasse voor het spel "Galgje" - Gemaakt door Jens
class HangmanGame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.create_widgets()  # Initialiseer de interfacecomponenten

    # Methode om de interfacecomponenten te creëren
    def create_widgets(self):
        # Lijst met woorden om te raden
        self.word_list = ["python", "programmeur", "scrum", "widget", "functie", "alex-jonkhart", "boolean", "greg", 
                          "kanyingwest", "aanvallenjongens", "clashofclans"]
        self.new_game()  # Start een nieuw spel

    # Methode om een nieuw spel te starten
    def new_game(self):
        # Kies willekeurig een woord uit de lijst en stel de spelstatus in
        self.secret_word = random.choice(self.word_list)
        self.guessed_word = ["_"] * len(self.secret_word)  # Initieer een lijst met underscores voor niet-geraden letters
        self.guesses = set()  # Bewaar de geraden letters
        self.attempts_left = 6  # Zet het aantal pogingen op 6 (standaard bij Galgje)

        # Label met de titel van het spel
        self.label = tk.Label(self, text="Galgje", font=("Arial", 24))
        self.label.pack(pady=20)

        # Label dat het geraden woord toont
        self.word_label = tk.Label(self, text=" ".join(self.guessed_word), font=("Arial", 22))
        self.word_label.pack(pady=10)

        # Invoerveld voor de letter die de speler raadt
        self.entry = tk.Entry(self, font=("Arial", 22), width=5)
        self.entry.pack(pady=10)

        # Knop om de invoer van de speler te controleren
        self.guess_button = tk.Button(self, text="Gok", font=("Arial", 22), command=self.check_guess)
        self.guess_button.pack(pady=10)

        # Label dat het aantal resterende pogingen toont
        self.result_label = tk.Label(self, text=f"Pogingen over: {self.attempts_left}", font=("Arial", 22))
        self.result_label.pack(pady=10)

    # Methode om de gok van de speler te controleren
    def check_guess(self):
        guess = self.entry.get().lower()  # Haal de invoer op en zet deze om naar kleine letters

        # Controleer of de invoer een enkele letter is
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Fout", "Voer een enkele letter in")
            return

        # Controleer of de letter al eerder is geraden
        if guess in self.guesses:
            messagebox.showwarning("Let op", "Je hebt deze letter al geraden")
            return

        self.guesses.add(guess)  # Voeg de geraden letter toe aan de set

        # Als de letter in het geheime woord zit, werk dan het geraden woord bij
        if guess in self.secret_word:
            for i, letter in enumerate(self.secret_word):
                if letter == guess:
                    self.guessed_word[i] = guess
            self.word_label.config(text=" ".join(self.guessed_word))

            # Controleer of het hele woord geraden is
            if "_" not in self.guessed_word:
                messagebox.showinfo("Gefeliciteerd!", f"Je hebt het woord geraden: {self.secret_word}")
                self.new_game()  # Start een nieuw spel
        else:
            # Als de gok fout is, verlaag het aantal pogingen
            self.attempts_left -= 1
            self.result_label.config(text=f"Pogingen over: {self.attempts_left}")

            # Als de speler geen pogingen meer over heeft, toon een verliesbericht
            if self.attempts_left == 0:
                messagebox.showinfo("Verloren", f"Je hebt verloren! Het woord was: {self.secret_word}")
                self.new_game()  # Start een nieuw spel

# Hoofdapplicatie waarin beide spellen geïntegreerd zijn - Gemaakt door Bryan
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ontspanningstool")  # Zet de titel van het hoofdvenster
        self.geometry("700x600")  # Stel de grootte van het venster in
        self.create_menu()  # Maak het menu aan
        self.show_frame(NumberGuessingGame)  # Start standaard met het "Getallen raden" spel

    # Methode om het menu aan te maken
    def create_menu(self):
        menu_bar = tk.Menu(self)  # Creëer een menubalk
        self.config(menu=menu_bar)

        # Voeg een spelmenu toe aan de menubalk
        game_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Spellen", menu=game_menu)

        # Voeg opties toe aan het spelmenu voor elk spel
        game_menu.add_command(label="Getallen raden", command=lambda: self.show_frame(NumberGuessingGame))
        game_menu.add_command(label="Galgje", command=lambda: self.show_frame(HangmanGame))

    # Methode om het huidige frame te wisselen (tussen spellen)
    def show_frame(self, frame_class):
        new_frame = frame_class(self)  # Maak een nieuw frame aan voor het gekozen spel
        if hasattr(self, 'current_frame'):
            self.current_frame.pack_forget()  # Verberg het huidige frame
            self.current_frame.destroy()  # Verwijder het huidige frame
        self.current_frame = new_frame  # Zet het nieuwe frame als het huidige
        self.current_frame.pack(fill="both", expand=True)  # Toon het nieuwe frame

# Start de applicatie
if __name__ == "__main__":
    app = Application()
    app.mainloop()  # Start de hoofdloop van de applicatie
