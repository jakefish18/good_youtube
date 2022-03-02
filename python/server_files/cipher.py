"""
f - 9 таблица менделеева
i - 10 русский алфавит 
s - 19 английский алфавит 
h - 23 русский алфавит
e - 2 округленное значение e из математики
r - 18 русский алфавит
коэффицент умножения всего - 19 cумма элементов моего дня рождения
"""

def cipher(text: str) -> str:
    """
    Алгоритм шифровки основанный на значениях из документации.
    Сначала каждый код элемента умножается на значение из документации, значение определяется по порядковому значению.
    Если элемент за границой этих значений, то оно начинает умножатся сначала.
    Полученное значение умножается на общее значение и переводится обратно
    """
    nums_to_multiplication = [9, 10, 19, 23, 2, 18, 19] # значения из документации.
    general_multiplicator = 19

    result = ""
    multiplicator_index = 0

    for element in text:
        encrypted_element = ord(element) # Значение element
        encrypted_element *= nums_to_multiplication[multiplicator_index] * general_multiplicator
        encrypted_element %= 1114110
        encrypted_element = chr(encrypted_element)

        result += encrypted_element

        multiplicator_index += 1
        multiplicator_index %= 7
    
    return result
