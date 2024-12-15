import os
import shutil
import argparse
import random
import string
import logging
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import filedialog, messagebox

# Функція для очищення екрану
def clear_screen():
    """Очищає екран в залежності від операційної системи."""
    if os.name == 'nt':  # Для Windows
        os.system('cls')
    else:  # Для Linux/MacOS
        os.system('clear')

# Логування
logging.basicConfig(filename="file_sorter.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# 1. Запитуємо у користувача шляхи до директорій
def ask_user_dirs():
    """Запитує у користувача шляхи до вихідної та директорії призначення."""
    dist_dir = input("Введіть шлях до директорії 'dist' (де будуть створюватися файли) [за замовчуванням './dist']: ").strip() or './dist'
    sort_dir = input("Введіть шлях до директорії 'sort' (де файли будуть сортуватися) [за замовчуванням './sort']: ").strip() or './sort'

    # Перевірка на існування директорій
    while not os.path.exists(dist_dir):
        print(f"Директория {dist_dir} не існує.")
        create_dir = input(f"Бажаєте створити її? (y/n): ").strip().lower()
        if create_dir == 'y':
            os.makedirs(dist_dir)
            print(f"Директорія {dist_dir} створена.")
            break
        else:
            dist_dir = input(f"Введіть інший шлях до директорії {dist_dir}: ").strip()

    while not os.path.exists(sort_dir):
        print(f"Директория {sort_dir} не існує.")
        create_dir = input(f"Бажаєте створити її? (y/n): ").strip().lower()
        if create_dir == 'y':
            os.makedirs(sort_dir)
            print(f"Директорія {sort_dir} створена.")
            break
        else:
            sort_dir = input(f"Введіть інший шлях до директорії {sort_dir}: ").strip()

    return dist_dir, sort_dir

# 2. Запитуємо у користувача дозвіл на створення файлів
def ask_user_permission():
    """Запитує у користувача дозвіл на створення файлів і папок."""
    while True:
        response = input("Бажаєте, щоб початкові папки та файли були згенеровані? (y/n): ").strip().lower()
        if response == 'y':
            return True
        elif response == 'n':
            return False
        else:
            print("Невірна команда. Будь ласка, введіть 'y' для так або 'n' для ні.")

# 3. Запитуємо кількість файлів для створення
def ask_user_number_of_files():
    """Запитує кількість файлів для створення."""
    while True:
        try:
            num_files = int(input("Введіть кількість файлів для створення: "))
            if num_files <= 0:
                print("Кількість файлів повинна бути більшою за нуль.")
            else:
                return num_files
        except ValueError:
            print("Будь ласка, введіть коректне число.")

# 4. Генерація випадкового імені файлу з заданим розширенням
def generate_random_filename(extension):
    """Генерує випадкове ім'я файлу з заданим розширенням."""
    name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"{name}.{extension}"

# 5. Створення випадкових файлів у директорії 'dist'
def create_sample_files(dist_dir, num_files):
    """Створює випадкові файли в директорії 'dist'."""
    file_types = ['txt', 'docx', 'pdf', 'jpg', 'png', 'xlsx', 'exe', 'bat', 'ps1']
    files_created = 0
    
    # Перевіряємо, чи існує директорія dist, якщо ні — створюємо її
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)

    # Створюємо файли в директорії dist
    for _ in range(num_files):
        ext = random.choice(file_types)  # Вибір випадкового розширення
        filename = generate_random_filename(ext)
        file_path = os.path.join(dist_dir, filename)
        
        with open(file_path, 'w') as f:
            f.write(f"This is a sample {ext} file with a random name.")
        files_created += 1
        print(f"Файл {file_path} створений.")
    
    return files_created

# 6. Перевірка на дублікати файлів
def check_for_duplicates(sort_dir, file_name):
    """Перевіряє, чи існує вже файл з таким ім'ям у папці 'sort'."""
    for root, dirs, files in os.walk(sort_dir):
        if file_name in files:
            return True
    return False

# 7. Сортування файлів за розширенням та переміщення їх у відповідні підкаталоги
def sort_files(dist_dir, sort_dir, filter_ext=None):
    """Переміщає файли з dist до sort, сортує їх за розширенням."""
    files_moved = 0
    files_not_moved = []  # Список файлів, які не були переміщені
    created_dirs = set()  # Множина для збереження створених директорій
    
    try:
        # Перевіряємо, чи існує директорія для сортування, якщо ні — створюємо її
        if not os.path.exists(sort_dir):
            os.makedirs(sort_dir)

        # Перебираємо всі файли в директорії dist та її підкаталогах
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                if filter_ext and not file.endswith(tuple(filter_ext)):
                    continue  # Пропускаємо файли, які не відповідають фільтру за розширенням
                
                file_path = os.path.join(root, file)

                # Перевіряємо на дублікати перед переміщенням
                if check_for_duplicates(sort_dir, file):
                    print(f"Файл {file} вже існує в папці sort. Пропускаємо.")
                    files_not_moved.append((file, "Файл з таким ім'ям вже існує в папці sort."))
                    continue
                
                # Отримуємо розширення файлу
                ext = file.split('.')[-1]
                ext_dir = os.path.join(sort_dir, ext)
                
                # Якщо папка для цього типу ще не створена, створюємо її
                if ext_dir not in created_dirs:
                    os.makedirs(ext_dir, exist_ok=True)
                    created_dirs.add(ext_dir)

                # Переміщаємо файл до відповідної папки
                dest_file_path = os.path.join(ext_dir, file)
                try:
                    shutil.move(file_path, dest_file_path)
                    files_moved += 1
                    print(f"Файл {file} переміщено в {dest_file_path}")
                except Exception as e:
                    files_not_moved.append((file, f"Помилка переміщення: {e}"))
                    print(f"Не вдалося перемістити файл {file}. Причина: {e}")

    except PermissionError as e:
        print(f"Permission Error: {e}")
    except FileNotFoundError as e:
        print(f"File Not Found Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

    return files_moved, files_not_moved

# 8. Підраховуємо кількість файлів у підкаталогах директорії
def count_files_in_subdirectories(dir_path):
    """Підраховує кількість файлів у підкаталогах директорії."""
    file_counts = {}
    
    # Перебираємо всі підкаталоги та рахуємо кількість файлів у кожному з них
    for root, dirs, files in os.walk(dir_path):
        if files:
            subdir = os.path.basename(root)
            file_counts[subdir] = len(files)
    
    return file_counts

# 9. Основна функція, що виконує логіку роботи скрипту
def main():
    # Очищаємо екран на початку роботи програми
    clear_screen()

    # Виведення інформації про можливості запуску скрипту з аргументами командного рядка
    print("Скрипт може працювати з аргументами командного рядка.")
    print("Приклад використання:")
    print("python task1.py ./dist ./sort")
    print("або для абсолютних шляхів:")
    print("python task1.py C:\\dist C:\\sort")
    print("Якщо аргументи не передано, буде використано інтерактивний режим.")

    # Ініціалізація парсера аргументів командного рядка
    parser = argparse.ArgumentParser(description='Копіює файли та сортує за розширенням.')
    
    # Додаємо аргументи для шляху до директорій
    parser.add_argument('dist_dir', type=str, nargs='?', default='./dist', help='Шлях до директорії "dist" для створення файлів')
    parser.add_argument('sort_dir', type=str, nargs='?', default='./sort', help='Шлях до директорії "sort" для сортування файлів')
    parser.add_argument('--filter', type=str, nargs='+', help='Фільтрація файлів за розширенням (наприклад: txt pdf png)')
    args = parser.parse_args()

    # Перевірка, чи були передані аргументи
    if args.dist_dir == './dist' or args.sort_dir == './sort':
        print("Аргументи не були передані. Запускаємо інтерактивний режим...")
        if ask_user_permission():
            # Якщо користувач бажає, генеруємо файли
            num_files = ask_user_number_of_files()
            files_created = create_sample_files(args.dist_dir, num_files)

            # Сортуємо файли після їх створення
            files_moved, files_not_moved = sort_files(args.dist_dir, args.sort_dir, filter_ext=args.filter)

            # Підрахунок файлів у підкаталогах
            file_counts = count_files_in_subdirectories(args.sort_dir)

            # Виведення статистики
            print("\nСтатистика:")
            print(f"Згенеровано файлів у dist: {files_created}")
            print(f"Переміщено файлів у sort: {files_moved}")
            print("\nКількість файлів у підкаталогах:")
            for ext, count in file_counts.items():
                print(f"{ext}: {count} файлів")

            # Виведення файлів, які не були переміщені
            if files_not_moved:
                print("\nФайли, які не були переміщені:")
                for file, reason in files_not_moved:
                    print(f"{file}: Причина - {reason}")
            
            # Запит користувача, чи потрібно завершити роботу
            while True:
                continue_working = input("\nБажаєте завершити роботу? (y/n): ").strip().lower()
                if continue_working == 'y':
                    print("Дякуємо за використання скрипту. Завершуємо роботу.")
                    break
                elif continue_working == 'n':
                    clear_screen()  # Очищаємо екран перед повторним запуском
                    main()  # Перезапускаємо програму
                    break
                else:
                    print("Невірна команда. Будь ласка, введіть 'y' для завершення або 'n' для продовження.")
        else:
            # Якщо користувач відмовляється, запитуємо шляхи для сортування файлів
            dist_dir, sort_dir = ask_user_dirs()
            files_moved, files_not_moved = sort_files(dist_dir, sort_dir)
            
            # Підрахунок файлів в підкаталогах
            file_counts = count_files_in_subdirectories(sort_dir)
            
            # Виведення статистики
            print("\nСтатистика після виконання:")
            print(f"Переміщено файлів у sort: {files_moved}")
            print("\nКількість файлів у підкаталогах:")
            for ext, count in file_counts.items():
                print(f"{ext}: {count} файлів")

            # Виведення файлів, які не були переміщені, якщо є
            if files_not_moved:
                print("\nФайли, які не були переміщені:")
                for file, reason in files_not_moved:
                    print(f"{file}: Причина - {reason}")
            
            # Запит користувача, чи потрібно завершити роботу
            while True:
                continue_working = input("\nБажаєте завершити роботу? (y/n): ").strip().lower()
                if continue_working == 'y':
                    print("Дякуємо за використання скрипту. Завершуємо роботу.")
                    break
                elif continue_working == 'n':
                    clear_screen()  # Очищаємо екран перед повторним запуском
                    main()  # Перезапускаємо програму
                    break
                else:
                    print("Невірна команда. Будь ласка, введіть 'y' для завершення або 'n' для продовження.")
    else:
        print("Аргументи були передані. Починаємо сортування файлів...")
        if args.dist_dir and args.sort_dir:
            files_moved, files_not_moved = sort_files(args.dist_dir, args.sort_dir, filter_ext=args.filter)
            # Підрахунок файлів в підкаталогах
            file_counts = count_files_in_subdirectories(args.sort_dir)
            
            # Виведення статистики
            print("\nСтатистика після виконання:")
            print(f"Переміщено файлів у sort: {files_moved}")
            print("\nКількість файлів у підкаталогах:")
            for ext, count in file_counts.items():
                print(f"{ext}: {count} файлів")

            # Виведення файлів, які не були переміщені
            if files_not_moved:
                print("\nФайли, які не були переміщені:")
                for file, reason in files_not_moved:
                    print(f"{file}: Причина - {reason}")

if __name__ == '__main__':
    main()
