import tkinter as tk
import random

class HangmanGame:
    #создание главного окна:
    def __init__(self, root):
        self.root = root 
        self.root.title("Виселица")
        self.root.geometry("600x500")
        self.root.resizable(False, False) #запрет изменения окна
    #введение слов для угадывания, запрещенные буквы, использованные, угаданные, попытки
        self.words = ['программирование', 'алгоритмизация', 'кодирование', 'информация', 'компьютер', 'клавиатура']
        self.vowels = 'ауоыиэяюёе'
        self.max_turns = 6
        self.secret_word = ''
        self.guessed_letters = []  
        self.used_letters = []          
        self.turns_left = self.max_turns
        self.game_active = True
    #рисунок для ошибок, список
        self.gallows = [
            """
     ------
     |    |
     |
     |
     |
     |
     |
    ----------
    """,
            """
     ------
     |    |
     |    O
     |
     |
     |
     |
    ----------
    """,
            """
     ------
     |    |
     |    O
     |    |
     | 
     |   
     |    
    ----------
    """,
            """
     ------
     |    |
     |    O
     |   /|
     |   
     |   
     |   
    ----------
    """,
            """
     ------
     |    |
     |    O
     |   /|\\
     |   
     |   
     |     
    ----------
    """,
            """
     ------
     |    |
     |    O
     |   /|\\
     |   /
     |   
     |    
    ----------
    """,
            """
     ------
     |    |
     |    O
     |   /|\\
     |   / \\
     |   
     |   
    ----------
    """
        ]
    #переменные для будующих оформленных окон
        self.word_label = None
        self.gallows_label = None
        self.used_label = None
        self.turns_label = None
        self.info_label = None
        self.entry = None
        self.guess_btn = None

        self.create_widgets() #создание виджетов
        self.new_game() #сама игра

    def create_widgets(self): #контейнеры для виселицы, букв, введения букв и прочего

        gallows_frame = tk.Frame(self.root)
        gallows_frame.pack(pady=10)

        self.gallows_label = tk.Label(gallows_frame, text="", font=("Courier", 12), justify=tk.LEFT)
        self.gallows_label.pack()

        word_frame = tk.Frame(self.root)
        word_frame.pack(pady=10)

        self.word_label = tk.Label(word_frame, text="", font=("Arial", 24))
        self.word_label.pack()

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Введите букву:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.entry = tk.Entry(input_frame, width=5, font=("Arial", 14), justify='center')
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind('<Return>', lambda event: self.guess_letter())

        self.guess_btn = tk.Button(input_frame, text="Угадать", command=self.guess_letter, font=("Arial", 12))
        self.guess_btn.pack(side=tk.LEFT, padx=5)

        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=10)

        self.turns_label = tk.Label(info_frame, text="", font=("Arial", 12))
        self.turns_label.pack()

        self.used_label = tk.Label(info_frame, text="", font=("Arial", 12), wraplength=500)
        self.used_label.pack()

        self.info_label = tk.Label(info_frame, text="", font=("Arial", 10), fg="blue")
        self.info_label.pack()

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        new_game_btn = tk.Button(control_frame, text="Новая игра", command=self.new_game, font=("Arial", 12))
        new_game_btn.pack(side=tk.LEFT, padx=10)

        rules_btn = tk.Button(control_frame, text="Правила", command=self.show_rules, font=("Arial", 12))
        rules_btn.pack(side=tk.LEFT, padx=10)

        stats_btn = tk.Button(control_frame, text="Статистика", command=self.show_stats, font=("Arial", 12))
        stats_btn.pack(side=tk.LEFT, padx=10)

        exit_btn = tk.Button(control_frame, text="Выход", command=self.root.quit, font=("Arial", 12))
        exit_btn.pack(side=tk.LEFT, padx=10)

    def new_game(self):
 
        self.secret_word = random.choice(self.words)
        self.guessed_letters = []
        self.used_letters = []
        self.turns_left = self.max_turns
        self.game_active = True

        for letter in self.secret_word:
            if letter in self.vowels and letter not in self.guessed_letters:
                self.guessed_letters.append(letter)

        self.update_display()
        self.info_label.config(text="Игра началась! Вводите согласные буквы.")
        self.entry.config(state='normal')
        self.guess_btn.config(state='normal')
        self.entry.delete(0, tk.END)
        self.entry.focus_set()

    def update_display(self):

        display_word = []
        for letter in self.secret_word:
            if letter in self.guessed_letters:
                display_word.append(letter)
            else:
                display_word.append('_')
        self.word_label.config(text=' '.join(display_word))

        errors = self.max_turns - self.turns_left
        self.gallows_label.config(text=self.gallows[errors])

        self.turns_label.config(text=f"Осталось попыток: {self.turns_left}")

        if self.used_letters:
            used_str = ', '.join(sorted(self.used_letters))
        else:
            used_str = 'пока нет'
        self.used_label.config(text=f"Использованные буквы: {used_str}")

        if self.game_active:
            if all(letter in self.guessed_letters for letter in self.secret_word):
                self.game_over(win=True)
            elif self.turns_left == 0:
                self.game_over(win=False)

    def guess_letter(self):

        if not self.game_active:
            return

        letter = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)

        if not letter:
            self.info_label.config(text="Вы ничего не ввели!", fg="red")
            return
        if len(letter) != 1:
            self.info_label.config(text="Введите одну букву!", fg="red")
            return
        if not ('а' <= letter <= 'я'):
            self.info_label.config(text="Введите русскую букву!", fg="red")
            return
        if letter in self.used_letters:
            self.info_label.config(text="Эта буква уже была!", fg="red")
            return
        if letter in self.vowels:
            self.info_label.config(text="Гласные буквы уже открыты! Введите согласную.", fg="red")
            return

        self.used_letters.append(letter)

        if letter in self.secret_word:
            if letter not in self.guessed_letters:
                self.guessed_letters.append(letter)
            self.info_label.config(text="Есть такая буква!", fg="green")
        else:
            self.turns_left -= 1
            self.info_label.config(text="Такой буквы нет.", fg="red")

        self.update_display()

    def game_over(self, win):
        
        self.game_active = False
        self.entry.config(state='disabled')
        self.guess_btn.config(state='disabled')

        if win:
            message = f"Поздравляем! Вы выиграли!\nЗагаданное слово: {self.secret_word}"
        else:
            message = f"Вы проиграли.\nЗагаданное слово: {self.secret_word}"

        self.info_label.config(text=message, fg="purple")

    def show_rules(self):
        
        rules_window = tk.Toplevel(self.root)
        rules_window.title("Правила")
        rules_window.geometry("300x150")
        rules_window.resizable(False, False)

        tk.Label(rules_window, text="", font=("Arial", 14), fg="gray").pack(expand=True)
        tk.Button(rules_window, text="Закрыть", command=rules_window.destroy).pack(pady=10)

    def show_stats(self):
    
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Статистика")
        stats_window.geometry("300x150")
        stats_window.resizable(False, False)

        tk.Label(stats_window, text="", font=("Arial", 14), fg="gray").pack(expand=True)
        tk.Button(stats_window, text="Закрыть", command=stats_window.destroy).pack(pady=10)


root = tk.Tk()
game = HangmanGame(root)
root.mainloop()