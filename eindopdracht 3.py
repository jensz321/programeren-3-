import tkinter as tk
from tkinter import messagebox
import random

class NumberGuessingGame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Raad een getal tussen 1 en 100")
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.guess_button = tk.Button(self, text="Gok", command=self.check_guess)
        self.guess_button.pack()

        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

        self.new_game()

    def new_game(self):
        self.secret_number = random.randint(1, 100)
        self.guess_count = 0
        self.result_label.config(text="")

    def check_guess(self):
        try:
            guess = int(self.entry.get())
            self.guess_count += 1

            if guess < self.secret_number:
                self.result_label.config(text="Te laag!")
            elif guess > self.secret_number:
                self.result_label.config(text="Te hoog!")
            else:
                self.result_label.config(text=f"Goed geraden! Je deed {self.guess_count} pogingen.")
                messagebox.showinfo("Gefeliciteerd!", f"Je hebt het getal geraden in {self.guess_count} pogingen!")
                self.new_game()

        except ValueError:
            messagebox.showerror("Fout", "Voer een geldig getal in")

class HangmanGame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.word_list = ["python", "programmeur", "scrum", "widget", "functie"]
        self.new_game()

    def new_game(self):
        self.secret_word = random.choice(self.word_list)
        self.guessed_word = ["_"] * len(self.secret_word)
        self.guesses = set()
        self.attempts_left = 6

        self.label = tk.Label(self, text="Galgje")
        self.label.pack()

        self.word_label = tk.Label(self, text=" ".join(self.guessed_word))
        self.word_label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.guess_button = tk.Button(self, text="Gok", command=self.check_guess)
        self.guess_button.pack()

        self.result_label = tk.Label(self, text=f"Pogingen over: {self.attempts_left}")
        self.result_label.pack()

    def check_guess(self):
        guess = self.entry.get().lower()

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Fout", "Voer een enkele letter in")
            return

        if guess in self.guesses:
            messagebox.showwarning("Let op", "Je hebt deze letter al geraden")
            return

        self.guesses.add(guess)

        if guess in self.secret_word:
            for i, letter in enumerate(self.secret_word):
                if letter == guess:
                    self.guessed_word[i] = guess
            self.word_label.config(text=" ".join(self.guessed_word))

            if "_" not in self.guessed_word:
                messagebox.showinfo("Gefeliciteerd!", f"Je hebt het woord geraden: {self.secret_word}")
                self.new_game()
        else:
            self.attempts_left -= 1
            self.result_label.config(text=f"Pogingen over: {self.attempts_left}")

            if self.attempts_left == 0:
                messagebox.showinfo("Verloren", f"Je hebt verloren! Het woord was: {self.secret_word}")
                self.new_game()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ontspanningstool")
        self.geometry("400x300")
        self.create_menu()
        self.show_frame(NumberGuessingGame)

    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        game_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Spellen", menu=game_menu)

        game_menu.add_command(label="Getallen raden", command=lambda: self.show_frame(NumberGuessingGame))
        game_menu.add_command(label="Galgje", command=lambda: self.show_frame(HangmanGame))

    def show_frame(self, frame_class):
        new_frame = frame_class(self)
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
