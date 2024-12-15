import turtle
import logging
import time
import os

# Логування
logging.basicConfig(filename="koch_snowflake.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Очищення екрану в консолі в залежності від ОС
def clear_screen():
    """Очищає екран в залежності від операційної системи."""
    if os.name == 'nt':  # Для Windows
        os.system('cls')
    else:  # Для Linux та інших UNIX-подібних систем
        os.system('clear')

# Функція для побудови сніжинки Коха
def koch_snowflake(t, order, size):
    """Рекурсивна функція для малювання сніжинки Коха."""
    if order == 0:
        t.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_snowflake(t, order - 1, size / 3)
            t.left(angle)

# Функція для ініціалізації малювання
def draw_snowflake(order, size, color, speed):
    """Малює сніжинку Коха для заданого порядку та розміру, кольору і швидкості."""
    screen = turtle.Screen()
    screen.bgcolor("white")
    t = turtle.Turtle()
    t.color(color)
    t.speed(speed)  # Швидкість малювання
    t.penup()
    t.goto(-size / 2, size / 3)
    t.pendown()

    logging.info(f"Розпочато малювання сніжинки Коха з рівнем рекурсії {order}, розміром {size}, кольором {color}, швидкістю {speed}")

    start_time = time.time()  # Початок вимірювання часу

    for _ in range(3):  # Малюємо три сторони рівностороннього трикутника
        koch_snowflake(t, order, size)
        t.right(120)  # Поворот для наступної сторони

    end_time = time.time()  # Кінець вимірювання часу
    elapsed_time = end_time - start_time  # Час, витрачений на малювання

    logging.info(f"Малювання сніжинки завершено. Час виконання: {elapsed_time:.2f} секунд.")

    turtle.done()

# Перевірка на введення цілих чисел
def input_integer(prompt, min_value=None, max_value=None, default_value=None):
    """Запитує ціле число у користувача з перевіркою введених даних."""
    while True:
        try:
            value = input(prompt)
            if value == "" and default_value is not None:
                return default_value  # Якщо значення не введено, використовується значення за замовчуванням
            value = int(value)
            if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                print(f"Будь ласка, введіть число в межах від {min_value} до {max_value}.")
            else:
                return value
        except ValueError:
            print("Будь ласка, введіть коректне ціле число.")

# Основна частина програми
def main():
    clear_screen()  # Очищаємо екран у консолі

    print("Малюємо сніжинку Коха.")

    # 1. Вибір кольору ліній
    color = input("Введіть колір ліній (за замовчуванням 'blue'): ").strip() or 'blue'
    while True:
        if color.isalpha():  # Перевірка на правильність введеного кольору
            break
        else:
            print("Будь ласка, введіть коректний колір для ліній.")
            color = input("Введіть колір ліній (за замовчуванням 'blue'): ").strip() or 'blue'
    logging.info(f"Вибрано колір ліній: {color}")

    # 2. Вибір рівня рекурсії з можливістю використання значення за замовчуванням
    order = input_integer("Введіть рівень рекурсії (позитивне ціле число, за замовчуванням 3): ", 0, 10, 3)
    logging.info(f"Вибрано рівень рекурсії: {order}")

    # 3. Вибір швидкості малювання
    speed = input_integer("Введіть швидкість малювання (від 1 до 10, за замовчуванням 5): ", 1, 10, 5)
    logging.info(f"Вибрана швидкість малювання: {speed}")

    # 4. Автоматичне налаштування рівня рекурсії в залежності від розміру екрану
    screen_width = turtle.window_width()
    if order > 5 and screen_width < 600:
        order = 5
        print("Занадто високий рівень рекурсії для невеликого екрану. Встановлено рівень рекурсії 5.")
        logging.info(f"Автоматично встановлено рівень рекурсії 5 через невеликий розмір екрану.")
    
    # 5. Вибір розміру сніжинки
    size = 400  # Початковий розмір сніжинки

    draw_snowflake(order, size, color, speed)

if __name__ == "__main__":
    main()
