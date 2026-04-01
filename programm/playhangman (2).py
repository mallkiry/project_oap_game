import tkinter as tk
import random
from tkinter import messagebox #всплывающие окна
import json #для загрузка статистики в файл
import os #для проверки существования файла
import logging

logging.basicConfig(
    filename='game.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

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
        self.stats_file = "hangman_stats.json"
        self.stats = self.load_stats()
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
        logging.info("Игра запущена")

    #статистика
    def load_stats(self):
        if os.path.exists(self.stats_file): #существует ли файл со статистикой
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                    return self.default_stats()
        else:
            return self.default_stats()

    def default_stats(self): #исходная статистика
        return {
            'games_played': 0,
            'wins': 0,
            'losses': 0,
            'total_guesses': 0,
            'correct_guesses': 0,
            'wrong_guesses': 0,
            'words_guessed': []
            }

    def save_stats(self): #сохранение статистики
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=4)

    def create_widgets(self): #контейнеры для виселицы, букв, введения букв и прочего
        #виселица
        gallows_frame = tk.Frame(self.root)
        gallows_frame.pack(pady=10)

        self.gallows_label = tk.Label(gallows_frame, text="", font=("Courier", 12), justify=tk.LEFT)
        self.gallows_label.pack()
        #слова
        word_frame = tk.Frame(self.root)
        word_frame.pack(pady=10)

        self.word_label = tk.Label(word_frame, text="", font=("Arial", 24))
        self.word_label.pack()
        #контейнер для поля ввода слова
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Введите букву:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.entry = tk.Entry(input_frame, width=5, font=("Arial", 14), justify='center')
        self.entry.pack(side=tk.LEFT, padx=5)
        #кнопка "угадать"
        self.guess_btn = tk.Button(input_frame, text="Угадать", command=self.guess_letter, font=("Arial", 12))
        self.guess_btn.pack(side=tk.LEFT, padx=5)

        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=10)

        self.turns_label = tk.Label(info_frame, text="", font=("Arial", 12))
        self.turns_label.pack()

        self.used_label = tk.Label(info_frame, text="", font=("Arial", 12), wraplength=500)
        self.used_label.pack()

        self.info_label = tk.Label(info_frame, text="", font=("Arial", 10), fg="white")
        self.info_label.pack()

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        #кнопка "новая игра"
        new_game_btn = tk.Button(control_frame, text="Новая игра", command=self.new_game, font=("Arial", 12))
        new_game_btn.pack(side=tk.LEFT, padx=10)
        #кнопка правил
        rules_btn = tk.Button(control_frame, text="Правила", command=self.show_rules, font=("Arial", 12))
        rules_btn.pack(side=tk.LEFT, padx=10)
        #кнопка статистика - подсчет побед
        stats_btn = tk.Button(control_frame, text="Статистика", command=self.show_stats, font=("Arial", 12))
        stats_btn.pack(side=tk.LEFT, padx=10)
        #кнопка выхода
        exit_btn = tk.Button(control_frame, text="Выход", command=self.root.quit, font=("Arial", 12))
        exit_btn.pack(side=tk.LEFT, padx=10)
    #функция игры самой
    def new_game(self):
 
        self.secret_word = random.choice(self.words)
        self.guessed_letters = []
        self.used_letters = []
        self.turns_left = self.max_turns
        self.game_active = True
    #перебор букв в слове, вывод гласных в угаданное для вывода(подсказки)
        for letter in self.secret_word:
            if letter in self.vowels and letter not in self.guessed_letters:
                self.guessed_letters.append(letter)
    #подготовка к возможности игрока вводить символы
        self.update_display()
        self.info_label.config(text="Игра началась! Вводите согласные буквы.")
        self.entry.config(state='normal')
        self.guess_btn.config(state='normal')
        self.entry.delete(0, tk.END)
        self.entry.focus_set()
        logging.info(f"Новая игра. Загадано слово: {self.secret_word} (гласные открыты)")
    #вывод использованных букв, ошибок, правильных букв
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
    #проверка веденных букв
    def guess_letter(self):

        if not self.game_active:
            return

        letter = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)

        if not letter:
            self.info_label.config(text="Вы ничего не ввели!", fg="red")
            logging.info("Попытка ввода пустой строки")
            return
        if len(letter) != 1:
            self.info_label.config(text="Введите одну букву!", fg="red")
            logging.info(f"Попытка ввода более одной буквы: {letter}")
            return
        if not ('а' <= letter <= 'я'):
            self.info_label.config(text="Введите русскую букву!", fg="red")
            logging.info(f"Попытка ввода не русской буквы: {letter}")
            return
        if letter in self.used_letters:
            self.info_label.config(text="Эта буква уже была!", fg="red")
            logging.info(f"Повторный ввод буквы: {letter}")
            return
        if letter in self.vowels:
            self.info_label.config(text="Гласные буквы уже открыты! Введите согласную.", fg="red")
            logging.info(f"Попытка ввести гласную: {letter}")
            return
        self.stats['total_guesses'] += 1
        self.used_letters.append(letter)
        if letter in self.secret_word:
            if letter not in self.guessed_letters:
                self.guessed_letters.append(letter)
            self.stats['correct_guesses'] += 1
            self.info_label.config(text="Есть такая буква!", fg="green")
            logging.info(f"Буква '{letter}' есть в слове")
        else:
            self.turns_left -= 1
            self.stats['wrong_guesses'] += 1
            self.info_label.config(text="Такой буквы нет.", fg="red")
            logging.info(f"Буква '{letter}' отсутствует в слове, осталось попыток: {self.turns_left}")

        self.update_display()
        self.save_stats()
    #победа или проигрыш
    def game_over(self, win):
        
        self.game_active = False
        self.entry.config(state='disabled')
        self.guess_btn.config(state='disabled')
        self.stats['games_played'] += 1
        if win:
            self.stats['wins'] += 1
            self.stats['words_guessed'].append(self.secret_word)
            message = f"Поздравляем! Вы выиграли!\nЗагаданное слово: {self.secret_word}"
            logging.info(f"Победа! Слово '{self.secret_word}' угадано")
        else:
            self.stats['losses'] += 1
            message = f"Вы проиграли.\nЗагаданное слово: {self.secret_word}"
            logging.info(f"Поражение. Загаданное слово: {self.secret_word}")

        self.info_label.config(text=message, fg="white")
        self.save_stats()
        self.show_game_over_window(win)
    #окно  победы или проигрыша
    def show_game_over_window(self, win):
        over_window = tk.Toplevel(self.root)
        over_window.title("Игра окончена")
        over_window.geometry("300x150")
        over_window.resizable(False, False)
        over_window.grab_set()

        if win:
            result_text = "Победа!"
        else:
            result_text = "Поражение."

        tk.Label(over_window, text=f"{result_text}\nЗагаданное слово: {self.secret_word}",
                 font=("Arial", 12), wraplength=280, pady=10).pack()

        btn_frame = tk.Frame(over_window)
        btn_frame.pack(pady=10)
        def new_game_and_close():
            self.new_game()
            over_window.destroy()
            logging.info("Окно окончания игры закрыто, начата новая игра")
        tk.Button(btn_frame, text="Новая игра", command=new_game_and_close, font=("Arial", 12), width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Закрыть",
                  command=lambda: (over_window.destroy(), logging.info("Окно окончания игры закрыто")),  # добавлено логирование
                  font=("Arial", 12), width=12).pack(side=tk.LEFT, padx=5)
        logging.info(f"Открыто окно окончания игры: {result_text}")
    #окно правил
    def show_rules(self):
        
        rules_window = tk.Toplevel(self.root)
        rules_window.title("Правила")
        rules_window.geometry("400x250")
        rules_window.resizable(False, False)
        rules_text = (
            "Правила игры «Виселица»:\n\n"
            "1. Вам загадано слово по теме ИТ.\n"
            "2. Гласные буквы открыты сразу.\n"
            "3. Вы должны угадать согласные буквы, вводите их по 1.\n"
            "4. Если буква угадана верно, она выведется в слово.\n"
            "5. Если нет, рисутеся виселица.\n"
            "6. Всего даётся 6 попыток.\n"
            "7. Выигрыш — слово открыто полностью.\n"
            "8. Проигрыш — попытки закончились, вы кого-то повесили(."
        )

        tk.Label(rules_window, text=rules_text, font=("Arial", 11), justify=tk.LEFT, padx=10, pady=10).pack(anchor='w')
        tk.Button(rules_window, text="Закрыть",
                  command=lambda: (rules_window.destroy(), logging.info("Окно правил закрыто")),  # добавлено логирование
                  font=("Arial", 12)).pack(pady=10)
        logging.info("Открыто окно правил")
    #окно статистики
    def show_stats(self):
    
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Статистика")
        stats_window.geometry("500x350")
        stats_window.resizable(False, False)

        tk.Label(stats_window, text="Статистика игр", font=("Arial", 16, "bold")).pack(pady=10)
        stats_frame = tk.Frame(stats_window)
        stats_frame.pack(pady=10, padx=20, fill=tk.BOTH)

        #оформление статистики
        win_percent = 0
        if self.stats['games_played'] > 0:
            win_percent = (self.stats['wins'] / self.stats['games_played']) * 100
        stats_text = (
            f"Сыграно игр: {self.stats['games_played']}\n"
            f"Побед: {self.stats['wins']}\n"
            f"Поражений: {self.stats['losses']}\n"
            f"Процент побед: {win_percent:.1f}%\n"
            f"Всего попыток: {self.stats['total_guesses']}\n"
            f"Верных букв: {self.stats['correct_guesses']}\n"
            f"Ошибок: {self.stats['wrong_guesses']}\n"
            f"Угаданные слова: {len(self.stats['words_guessed'])}"
        )

        tk.Label(stats_frame, text=stats_text, font=("Arial", 12), justify=tk.LEFT).pack(anchor=tk.W)
        #последние угаданные слова
        if self.stats['words_guessed']:
            last_words = self.stats['words_guessed'][-5:]
            words_str = ", ".join(last_words)
            tk.Label(stats_window, text=f"Последние слова:\n{words_str}", font=("Arial", 10), wraplength=350, justify=tk.CENTER).pack(pady=10)

        btn_frame = tk.Frame(stats_window)
        btn_frame.pack(pady=10)
        def reset_and_log():
            self.reset_stats_confirmation()
        tk.Button(btn_frame, text="Сбросить статистику", command=reset_and_log, font=("Arial", 12), bg="lightcoral").pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Закрыть",
                  command=lambda: (stats_window.destroy(), logging.info("Окно статистики закрыто")),  # добавлено логирование
                  font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        logging.info("Открыто окно статистики")

    #окно сброса статистики
    def reset_stats_confirmation(self):
        result = messagebox.askyesno("Сброс статистики", "Вы уверены, что хотите обнулить всю статистику?")
        if result:
            self.stats = self.default_stats()
            self.save_stats()
            logging.info("Статистика сброшена пользователем")
            messagebox.showinfo("Статистика", "Статистика сброшена.")
        else:
            logging.info("Сброс статистики отменён")

root = tk.Tk() #главное окно
game = HangmanGame(root)#окно внутри класса, редактирование интерфейса
root.protocol("WM_DELETE_WINDOW", lambda: (logging.info("Приложение закрыто пользователем"), root.destroy()))
root.mainloop() #цикличная работа интерфейса