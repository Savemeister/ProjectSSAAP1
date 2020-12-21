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
