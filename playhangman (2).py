import random
words = ['программирование', 'алгоритмизация', 'кодирование', 'информация', 'компьютер', 'клавиатура']
secretword = random.choice(words)
field = (
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
)
def hangman():
    print(field[0]) 
    print ('Привет! Добро пожаловать в игру "Виселица". Твоя задача - угадать за 5 попыток слово. '
           'Гласные буквы уже известны. Угадывай только согласные букввы. Удачи!')
    vowels = 'ауоыиэяюёе'
    english = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    turn = 6
    use = []
    while turn > 0:
        missed = 0
        for letter in secretword:
            if letter in vowels:
                print (letter,end=' ')
            else:
                print ('_',end=' ')
                missed += 1
        if missed == 0:
            print ('\nТы выиграл!')
            break
        guess = input("\nНазови букву:")
        if guess in english:
            print("Ввод только русских букв")
            guess = input("\nНазови дуругю букву:")
        elif guess in vowels:
            print("Эта буква уже есть")
            guess = input("\nНазови другую букву:")
        vowels += guess 
        use += guess 
        if guess not in secretword:
            turn -= 1
            print ('\Не угадал.')
            print ('\nОсталось попыток:', turn)
            print('\nТы использовал буквы:', use)
        if turn < 6: print (field[1])
        if turn < 5: print (field[2])
        if turn < 4: print (field[3])
        if turn < 3: print (field[4])
        if turn < 2: print (field[5])
        if turn < 1: print (field[6])
        if turn == 0: print ('\n\nЭто слово: ', secretword)
answer = 'да'
while answer == 'да':
    secretword = random.choice(words)
    hangman()
    print('Хочешь сыграть снова? (да или нет)')
    answer = input()
    if answer == 'нет':
        print("Пока!")
        break