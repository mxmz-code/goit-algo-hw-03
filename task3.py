import logging
import time
import os

# Логування
logging.basicConfig(filename="hanoi_towers.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Очищення екрану в консолі в залежності від ОС
def clear_screen():
    """Очищає екран в залежності від операційної системи."""
    if os.name == 'nt':  # Для Windows
        os.system('cls')
    else:  # Для Linux та інших UNIX-подібних систем
        os.system('clear')

# Функція для переміщення одного диска
def move_disk(source, target, pegs, draw_graphics, draw_ascii):
    """Переміщує диск і виводить стан у консоль або псевдографіку."""
    disk = pegs[source].pop()  # Витягти диск з початкового стрижня
    pegs[target].append(disk)  # Помістити його на цільовий стрижень
    global step_counter
    step_counter += 1  # Збільшуємо лічильник кроків
    
    # Оновлення графіки або псевдографіки
    if draw_graphics:
        update_visual(pegs)
    elif draw_ascii:
        update_ascii(pegs)
    
    # Виведення стану в консоль (для текстового режиму)
    if not draw_graphics and not draw_ascii:
        print(f"Перемістити диск з {source} на {target}: {disk}")
        print(f"Проміжний стан: {pegs}")

# Псевдографічне відображення стану
def update_ascii(pegs):
    """Оновлює псевдографічне відображення стрижнів та дисків."""
    print("\nПоточний стан:")
    for peg, discs in pegs.items():
        print(f"{peg}: ", end="")
        if discs:
            print(" ".join([f"({disk})" for disk in discs]))
        else:
            print("Порожній")
    print("\n")

# Оновлення графіки (не використовується в псевдографічному режимі)
def update_visual(pegs):
    """Оновлює графічне відображення стрижнів та дисків."""
    print(f"Поточний стан: {pegs}")  # Можна додати графічні малюнки тут (тільки для графічного режиму)

# Рекурсивна функція для переміщення дисків
def hanoi(n, source, target, auxiliary, pegs, draw_graphics, draw_ascii):
    """Рекурсивна функція для переміщення дисків з одного стрижня на інший."""
    if n == 1:
        move_disk(source, target, pegs, draw_graphics, draw_ascii)
    else:
        hanoi(n - 1, source, auxiliary, target, pegs, draw_graphics, draw_ascii)
        move_disk(source, target, pegs, draw_graphics, draw_ascii)
        hanoi(n - 1, auxiliary, target, source, pegs, draw_graphics, draw_ascii)

# Функція для вводу цілих чисел з перевіркою
def input_integer(prompt, min_value=1, max_value=None):
    """Запитує ціле число з перевіркою на коректність."""
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Будь ласка, введіть число більше або рівне {min_value}.")
            elif max_value is not None and value > max_value:
                print(f"Будь ласка, введіть число менше або рівне {max_value}.")
            else:
                return value
        except ValueError:
            print("Будь ласка, введіть коректне ціле число.")

def main():
    clear_screen()  # Очищаємо екран у консолі

    print("Малюємо Ханойські башти.")
    print("Вибір налаштувань для Ханойських башт.")
    
    # 1. Вибір типу виведення (Текстове або Псевдографіка)
    while True:
        try:
            draw_type = int(input("Виберіть тип виведення:\n1. Текстове (консоль)\n2. Псевдографіка\nВведіть 1 або 2: "))
            if draw_type == 1:
                draw_graphics = False
                draw_ascii = False  # Якщо вибрано текстовий варіант, графіка не використовується
                break
            elif draw_type == 2:
                draw_ascii = True  # Якщо вибрано псевдографіку, активуємо її
                draw_graphics = False
                break
            else:
                print("Невірний вибір! Будь ласка, введіть 1 або 2.")
        except ValueError:
            print("Будь ласка, введіть коректне число: 1 або 2.")
    
    # 2. Вибір кількості дисків
    n = input_integer("Введіть кількість дисків на початковому стрижні (позитивне ціле число): ", 1)

    # Створюємо початковий стан стрижнів
    pegs = {'A': list(range(n, 0, -1)), 'B': [], 'C': []}
    print(f"Початковий стан: {pegs}")

    # Ініціалізація лічильника кроків
    global step_counter
    step_counter = 0

    # 3. Запуск рекурсії для переміщення дисків
    start_time = time.time()
    hanoi(n, 'A', 'C', 'B', pegs, draw_graphics, draw_ascii)
    end_time = time.time()

    # 4. Час виконання
    elapsed_time = end_time - start_time
    print(f"Малювання завершено. Кількість кроків: {step_counter}, час виконання: {elapsed_time:.2f} секунд.")
    logging.info(f"Малювання завершено. Кількість кроків: {step_counter}, час виконання: {elapsed_time:.2f} секунд.")

    print(f"Кінцевий стан: {pegs}")

if __name__ == "__main__":
    main()
