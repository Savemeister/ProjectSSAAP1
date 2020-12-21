import random


def MillerRabin(num, repeat = 5):
    """
    Функция вызывается в isPrime()
    Функция работает по алгоритму Миллера — Рабина. Она возвращает True, если num - простое число.
    Повторяет проверку repeat раз.
    Это необходимо для уменьшения вероятности ошибочного результата.
    Чем больше repeat, тем вероятнее верный результат.
    Но медленее проверка.
    """
    d = num - 1
    s = 0
    while d % 2 == 0:
        d = d // 2
        s += 1

    for _ in range(repeat):
        
        a = random.randrange(2, num - 1)
        v = pow(a, d, num)
        if v != 1: 
            i = 0
            while v != (num - 1):
                if i == s - 1:
                    return False
                else:
                    i += 1
                    v = (v ** 2) % num
    return True


def isPrime(num):
    """
    Дело в том, что тест Миллера — Рабина хоть и относительно быстр.
    Этой скорости может быть недостаточно.
    Поэтому существуют ещё один метод проверки на простоту,
    который можно использовать до теста Миллера - Рабина.
    Подробнее ниже.
    """
    if (num < 2):
        return False # 0, 1 и отрицательные числа не являются простыми

    # Смысл заключается в том, что мы делим наше число
    # На несколько первых простых чисел, до 1000
    # Если поделилось, то наше число точно не простое
    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
                 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137,
                 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277,
                 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
                 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439,
                 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521,
                 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607,
                 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683,
                 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773,
                 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863,
                 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967,
                 971, 977, 983, 991, 997]

    # Смотрим есть ли наше число в lowPrimes
    if num in lowPrimes:
        return True

    # Проверяем делимость нашего числа на небольшие простые числа.
    for prime in lowPrimes:
        if (num % prime == 0):
            return False

    # Если это не дало результатов, то используем тест Миллера — Рабина
    return MillerRabin(num)


def GeneratingBigPrime(keysize = 1024):
    # Возвращает простое число заданного размера бит.
    while 1:
        num = random.getrandbits(keysize)
        if isPrime(num):
            return num


def CoprimeTest(z,E): # Тест на простоту
    while z != 0 and E != 0:
        if z > E:
            z %= E
        else:
            E %= z
    if z + E == 1:
        return True
    else:
        return False

def GeneratingE(z): # Генерация E
    while 1:
        E = random.randint(1_000_000_000, 100_000_000_000)
        if CoprimeTest(z, E) == True:
            return E

"""
Непростой момент в этой программе. Встала
проблема, как преобразовать слова в цифру.
Причём, нужно чтобы получилось не несколько цифр,
отвечающих за каждую букву. А одна цифра, отвечающая
за всё слово целиком. Ведь несколько цифр передавать,
это слишком много данных. И к тому же, это уменьшает
криптографическую стойкость. Ведь будут одинаковые
цифры отвечающие за одинаковые буквы. И можно будет угадать,
какая за какую.

Было придуманно разбить численные представления букв Юникода
по 4 цифры. Добовляя в начале трёх и менее значных чисел нули.
"""
def Encryption(message): # Шифрование
    emessage = ""
    for i in message:
        i = str(ord(i))
        if len(i) == 1:
            i = "000" + i
        elif len(i) == 2:
            i = "00" + i
        elif len(i) == 3:
            i = "0" + i
        emessage += i
    emessage = "1" + emessage
    # Чтобы нули в начале не потерялись
    # И от этого не сбилось наше разбиение
    # Добовляем в начало единицу
    emessage = pow(int(emessage), E, n)
    return emessage


def Decryption(emessage): # Дешифрование
    emessage = str(pow(emessage, D, n))
    emessage = emessage[1:]
    # Удаляем в начале, добаленную нами ранее,
    # единицу
    s = 0 # Счётчик, отсчитывающий по четыре цифры
    ch = True # Значение для контроля удаления нулей в начале
    # четырёх значного числа
    dmessage = ""
    bukva = ""
    for i in emessage:
        s += 1
        if i == "0" and ch:
            continue
        bukva += i
        ch = False
        if s == 4:
            ch = True
            s = 0
            dmessage += chr(int(bukva))
            bukva = ""
    return dmessage
    

def GeneratingD(E, z, n): # Генерация D
    D = pow(E, -1, z)
    return D

def newkeys(): # Генерация новых ключей
    p, q = GeneratingBigPrime(), GeneratingBigPrime()
    z = (p-1) * (q-1)
    n = p * q
    E = GeneratingE(z)
    defoltE = 65537
    D = GeneratingD(E, z, n)
    return n, E, D, p, q


#Запись всех полученных ключей в текстовый файл.
def PrivateKeyRecording(n, E, D, p, q):
    txt = input("Название файла для записи: ")
    with open(txt + ".txt", "w") as t:
        t.write("n = " + str(n) + "\n" +
                "E = " + str(E) + "\n" +
                "D = " + str(D) + "\n" +
                "p = " + str(p) + "\n" +
                "q = " + str(q))

#Запись только открытых ключей в текстовый файл.     
def PublicKeyRecording(n, E):
    txt = input("Название файла для записи: ")
    with open(txt + ".txt", "w") as t:
        t.write("n = " + str(n) + "\n" +
                "E = " + str(E) + "\n")
        

# Чтение всех сохранённых ключей из txt файла
def PrivateKeyReading():
    txt = input("Название файла для чтения: ")
    with open(txt + ".txt", "r") as t:
        n = int(t.readline().strip()[4:])
        E = int(t.readline().strip()[4:])
        D = int(t.readline().strip()[4:])
        p = int(t.readline().strip()[4:])
        q = int(t.readline().strip()[4:])
        return n, E, D, p, q
def PrivateOpenKeyReading():
    txt = input("Название файла для чтения: ")
    with open(txt + ".txt", "r") as t:
        n = int(t.readline().strip()[4:])
        E = int(t.readline().strip()[4:])
        return n, E


print("Приветствую, я реализация алгоритма RSA")
while 1:
    que1 = input("Что вы хотите сделать? \nЗашифровать сообщение(Введите з) или Дешифровать(Введите д) или же просто Сгенирировать ключи(Введите г): \n").lower()
    if que1 == "г" or que1 == "g":
        print("Генерация ключей.....")
        n, E, D, p, q = newkeys()
        print("n = " + str(n) + "\n" +
                "E = " + str(E) + "\n" +
                "D = " + str(D) + "\n" +
                "p = " + str(p) + "\n" +
                "q = " + str(q) + "\n")
        que4 = input("\nСохранить ключи? д/н\n")
        if que4 == "д":
            PrivateKeyRecording(n, E, D, p, q)
        que4 = input("\nСохранить ключи отдельно только открытые ключи? д/н\n")
        if que4 == "д":
            PublicKeyRecording(n, E)
        input()

    elif que1 == 'е' or que1 == 'e' or que1 == 'з':
        que2 = input("Вы хотите зашифровать сообщение с помощью ключей из файла(ф) \nили хотите ввести ключи в ручную(р)?\n").lower()
        if que2 == 'ф' or que2 == 'f':
            n, E = PrivateOpenKeyReading()
            message = input("Введите сообщение: ")
            emessage = Encryption(message)
            print("Зашифрованное сообщение: " + str(emessage))
            input()
        elif que3 == "p" or que3 == "r" or que3 == "р":
            n = int(input("n = "))
            E = int(input("E = "))
            message = input("Введите сообщение: ")
            emessage = Encryption(message)
            print("Зашифрованное сообщение: " + str(emessage))
            input()
        else:
            continue
    elif que1 == "д" or que2 == 'd':
        que3 = input("Вы хотите дешифровать сообщение с помощью ключей из файла(ф) или хотите ввести ключи в ручную(р)?\n").lower()
        if que3 == "ф" or que3 == "f":
            n, E, D, p, q = PrivateKeyReading()
            emessage = int(input("Введите шифр: "))
            demessage = Decryption(emessage)
            print("Дешифрованное сообщение: " + str(demessage))
            input()
        elif que3 == "p" or que3 == "r" or que3 == "р":
            D = int(input("D = "))
            n = int(input("n = "))
            emessage = int(input("Введите шифр: "))
            demessage = Decryption(emessage)
            print("Дешифрованное сообщение: " + str(demessage))
            input()
        else:
            continue
    else:
        continue


    




 


