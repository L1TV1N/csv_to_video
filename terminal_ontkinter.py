import tkinter as tk
from tkinter import scrolledtext
import sys
root = tk.Tk()
root.title("Результат выполнения кода")
root.geometry("800x600")
# Создание виджета ScrolledText для вывода результатов
new_data = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=30)
new_data.pack(expand=True, fill=tk.BOTH)

# Функция для перенаправления вывода
def redirect_output(text):
    new_data.insert(tk.END, text)
    new_data.see(tk.END)  # Прокручивает окно вниз
sys.stdout.write = redirect_output

# Здесь должен быть весь код для выполнения скрипта говна


# Восстановление стандартного вывода
sys.stdout = sys.__stdout__

# Запуск цикла обработки событий Tkinter
root.mainloop()
