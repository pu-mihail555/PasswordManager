import hashlib
import os
import random
import sqlite3
from tkinter import *
from tkinter import messagebox
from cryptography.fernet import Fernet

def get_window_size(root):
    # Получаем ширину экрана
    w = root.winfo_screenwidth()
    # Получаем высоту экрана
    h = root.winfo_screenheight()
    # Делим ширину на 2 без остатка
    w = w // 2
    # Тоже самое с высотой
    h = h // 2
    # Вычитаем 200 из ширины и высоты
    w = w - 200
    h = h - 200
    # Возвращаем ширину и высоту
    return w, h

#Абстрактный класс для работы с базой данных
class DataManager:
    # Функция для создания базы данных при первом запуске скрипта

    def execute_ddl_file(db_file, ddl_file):
        conn = sqlite3.connect('my_database.db')
        # Создается объект курсора(курсор это объект на основе объекта соединения, который используется для исполнения sql запросов)
        cur = conn.cursor()
        # Открытие DDL файла, и создание базы на его основе
        with open(ddl_file, 'r') as f:
            ddl_statements = f.read()
            cur.executescript(ddl_statements)
        # Коммитятся совершенные изменеия
        cur.commit()
        # Соединение закрывается
        cur.close()

# Функция для соединения с базой данных

    def sqlite_db_connect():
        # Создается объект соединения с базой данных, который принимает как аргумент строку с названием базы данных
        conn = sqlite3.connect('my_database.db')
        # Создается объект курсора(курсор это объект на основе объекта соединения, который используется для исполнения sql запросов)
        cur = conn.cursor()
        # Как итог функции возвращается курсор, для дальнейшей работы с ним
        return cur

# Функция для получения размера экрана, для последующего размещения окна в его центре



# Класс в котором описана логика генератора паролей


class PasswordGenerator:
    # Специальная функция, работает при создании экземпляра класса, для того чтобы присвоить ему значения по умолчанию
    # Например, при написании a = PasswordGenerator()
    # Объекту а по умолчанию присвоются некоторые значения, например если использовать print(a.isDigitTrue)
    # Вывод будет False
    # Объект self, который заключен в скобках, отвечает за экземпляр класса, например
    # Можно считать что вместо self, написано a, если учитывать ниже написанное
    def __init__(self):
        # Описываем флаги, для добавления чисел, больших букв и символов
        # по умолчанию все False, при нажатии checkButton, значения флагов меняются

        # Флаг для цифр
        self.isDigitTrue = False
        # Флаг для специальных символов
        self.isSymTrue = False
        # Флаг для больших букв
        self.isBigTrue = False

        # Заранее описываем строки с цифрами, символами и буквами
        self.digits = '0123456789'
        self.upcase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.symbols = '!@#$%^&*()_+'
        # Эти переменные нужны для флагов выше
        self.enabled_up = IntVar()
        self.enabled_dig = IntVar()
        self.enabled_sym = IntVar()

    # Функция для генерации паролей, принимает аргумент password_length_entry(Окно для ввода пароля)
    def generate_password(self, password_length_entry):
        # Изначальная строка из которой генерируется пароль
        self.lowkeys = 'abcdefghijklmnopqrstuvwxyz'
        # Получение длины пароля из окна для ввода пароля
        # если длина пароля есть, мы ее записываем в password_length
        try:
            password_length = int(password_length_entry.get())
        # Если ее нет, показываем сообщение ошибки
        except ValueError as e:
            messagebox.showerror("Ошибка", "Должна быть указана длина пароля!")
        # Проверка на флаги, если флаг включен, к изначальной строке добавляется выбранная строка
        if self.isBigTrue:
            self.lowkeys += self.upcase
        if self.isDigitTrue:
            self.lowkeys += self.digits
        if self.isSymTrue:
            self.lowkeys += self.symbols
        # Создаем сгенерированный пароль, на основе строки, и числа символов
        password = "".join(random.sample(self.lowkeys, password_length))
        # Возвращаем пароль
        return password

    # Функции для смены флагов
    def check_up(self):
        if self.enabled_up.get() == 1:
            self.isBigTrue = True
        else:
            self.isBigTrue = False

    def check_dig(self):
        if self.enabled_dig.get() == 1:
            self.isDigitTrue = True
        else:
            self.isDigitTrue = False

    def check_sym(self):
        if self.enabled_sym.get() == 1:
            self.isSymTrue = True
        else:
            self.isSymTrue = False


# Начальное окно для выбора одного из двух вариантов, в котором реализовано наследие из класса Frame, пакета tkinter
class OptionChoose(Frame, DataManager):
    # master=None, изначальное значение главного окна
    def __init__(self, master=None):
        # ключевое слово супер, можно мыслено поменять на слово Frame, оно устанавливает родителя,
        # и то что мы показываем родителю с помощью init на его родительское окно
        super().__init__(master)
        self.master = master

        self.pack(fill=BOTH, expand=1)
        self.master.resizable(False, False)
        # Создаем виджет кнопки
        choose_passrod_generator_button = Button(
            self, text="Сгенерировать пароль", command=self.choose_password_generator)
        # Пакуем кнопку в окно
        choose_passrod_generator_button.pack()

        choose_show_passwords_list = Button(
            self, text="Показать пароли", command=self.choose_show_passwords_list)
        choose_show_passwords_list.pack()

    # При выборе открыть окно с генератором паролей выбирается эта функция
    def choose_password_generator(self):
        # Уничтожается ныне открытое окно
        self.master.destroy()
        # Создается новый объект на основе класса Tk пакета tkinter
        new_root = Tk()
        # Используется функция для получения размера окна
        w, h = get_window_size(new_root)
        # Устанавливается позиция в пространстве и размер
        new_root.geometry(f'500x400+{w}+{h}')
        # Создается новый объект класса PasswordGeneratorWindow, с установкой родительского окна
        window = PasswordGeneratorWindow(master=new_root)
        # Запускам mainloop(), основной цикл программы
        new_root.mainloop()

    # При выборе открыть окно чтобы показать пароли выбирается эта функция
    def choose_show_passwords_list(self):
        # Создаем объект курсора
        c = DataManager.sqlite_db_connect()
        # исполняем sql запрос, выбрать все строки из таблицы паролей
        c.execute("SELECT * FROM passwords")
        # помещаем все что вернул запрос в переменную rows
        rows = c.fetchall()
        # Если в переменной rows что то есть, создаем новое окно с показом паролей
        if rows:
            # уничтожаем текущее окно
            self.master.destroy()

            new_root = Tk()
            w, h = get_window_size(new_root)
            new_root.geometry(f'500x400+{w}+{h}')
            window = DisplayPasswords(master=new_root)
            new_root.mainloop()
        # Если переменная rows пустая, соотвественно там нет ни одного пароля, показываем окно ошибки
        else:
            messagebox.showerror("Error", "Нет ни одного пароля")

# Класс для отображения паролей


class DisplayPasswords(Frame, DataManager):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Список паролей")
        self.pack(fill=BOTH, expand=1)
        self.master.resizable(False, False)
        # Создаем объект канвас
        self.canvas = Canvas(self)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # Создаем элемент для прокрутки экрана
        self.scrollbar = Scrollbar(
            self, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        
        

        self.frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor=NW)

        
        # Вызываем функцию для отображения паролей
        self.display_passwords()

        

    def display_passwords(self):
        # Смотрим все виджеты в окне, и уничтожаем их
        for widget in self.frame.winfo_children():
            widget.destroy()

        c = DataManager.sqlite_db_connect()
        c.execute("SELECT key FROM key")
        fernet_key = c.fetchone()[0].encode()

        c.execute("SELECT id, service, login, password FROM passwords")
        rows = c.fetchall()
        # enumerate означает, что мы проходим по массиву и получаем строку и ее счетчик
        # например:
        # a = [5, 5, 65, 2, 5]
        # for i, b in a:
        #   print(i, b)
        # вывод будет (1 5)
        #             (2 5)
        #             (3 65) и так далее
        for i, row in enumerate(rows):
            f = Fernet(fernet_key)
            decrypted_service = f.decrypt(row[1].encode()).decode()

            service_label = Label(self.frame, text=decrypted_service[:15])
            service_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            show_button = Button(self.frame, text="Показать", 
                                 command=lambda r=row: self.open_show_window(r))
            show_button.grid(row=i, column=1, padx=5, pady=5, sticky="e")

            # Кнопка для изменения
            edit_button = Button(self.frame, text="Изменить",
                                 command=lambda r=row: self.open_edit_window(r))
            edit_button.grid(row=i, column=2, padx=5, pady=5, sticky="e")
            # Кнопка для удаления
            delete_button = Button(
                self.frame, text="Удалить", command=lambda r=row: self.confirm_delete_record(r[0]))
            delete_button.grid(row=i, column=3, padx=5, pady=5, sticky="e")

        open_generator_button = Button(self.frame, text="Генератор паролей", command=self.open_password_generator)
        open_generator_button.grid(row=0, column=4, padx=5, pady=5)

        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    # Окно для подтвержения удаления записи

    def confirm_delete_record(self, record_id):
        confirm = messagebox.askokcancel(
            "Подтвердить", "Вы действительно хотите удалить?")
        if confirm:
            self.delete_record(record_id)
    # Функция для удаления записи

    def delete_record(self, record_id):
        c = DataManager.sqlite_db_connect()
        c.execute("DELETE FROM passwords WHERE id=?", (record_id,))
        c.connection.commit()
        self.display_passwords()
        messagebox.showinfo("Успех", "Данные обновлены успешно!")
    # Функция для открытия окна топлевел, для изменения данных записи

    def open_edit_window(self, row):
        c = DataManager.sqlite_db_connect()
        c.execute("SELECT key FROM key")
        fernet_key = c.fetchone()[0].encode()

        f = Fernet(fernet_key)
        decrypted_service = f.decrypt(row[1].encode()).decode()
        decrypted_login = f.decrypt(row[2].encode()).decode()
        decrypted_password = f.decrypt(row[3].encode()).decode()
        # Создание топлевел
        edit_window = Toplevel(self)
        w, h = get_window_size(self)
        # Устанавливается позиция в пространстве и размер
        edit_window.geometry(f'200x200+{w}+{h}')
        edit_window.title("Изменение объекта")
        # Создание трех окон ввода, для изменения данных
        service_entry = Entry(edit_window)
        service_entry.insert(0, decrypted_service)
        service_entry.grid(row=0, column=0, padx=10, pady=5)

        login_entry = Entry(edit_window)
        login_entry.insert(0, decrypted_login)
        login_entry.grid(row=1, column=0, padx=10, pady=5)

        password_entry = Entry(edit_window)
        password_entry.insert(0, decrypted_password)
        password_entry.grid(row=2, column=0, padx=10, pady=5)


        change_button = Button(edit_window, text="Изменить", command=lambda: self.update_password(
            row[0], service_entry.get(), login_entry.get(), password_entry.get(), edit_window, fernet_key))
        change_button.grid(row=3, column=0, padx=10, pady=5)

    def open_show_window(self, row):
        c = DataManager.sqlite_db_connect()
        c.execute("SELECT key FROM key")
        fernet_key = c.fetchone()[0].encode()

        f = Fernet(fernet_key)
        decrypted_service = f.decrypt(row[1].encode()).decode()
        decrypted_login = f.decrypt(row[2].encode()).decode()
        decrypted_password = f.decrypt(row[3].encode()).decode()
        # Создание топлевел окна
        show_window = Toplevel(self)
        w, h = get_window_size(self)
        # Устанавливается позиция в пространстве и размер
        show_window.geometry(f'200x200+{w}+{h}')
        show_window.title("Показать объект")
        # Создание трех окон ввода, для показа данных
        service_entry = Entry(show_window)
        service_entry.insert(0, decrypted_service)
        service_entry.config(state='readonly')
        service_entry.grid(row=0, column=0, padx=10, pady=5)
        Button(show_window, text="Коп.", command=lambda: service_entry.clipboard_append(service_entry.get())).grid(row=0, column=1)

        login_entry = Entry(show_window)
        login_entry.insert(0, decrypted_login)
        login_entry.config(state='readonly')
        login_entry.grid(row=1, column=0, padx=10, pady=5)
        Button(show_window, text="Коп.", command=lambda: login_entry.clipboard_append(login_entry.get())).grid(row=1, column=1)

        password_entry = Entry(show_window)
        password_entry.insert(0, decrypted_password)
        password_entry.config(state='readonly')
        password_entry.grid(row=2, column=0, padx=10, pady=5)
        Button(show_window, text="Коп.", command=lambda: password_entry.clipboard_append(password_entry.get())).grid(row=2, column=1)

    # Функция для обновления пароля

    def update_password(self, record_id, new_service, new_login, new_password, edit_window, fernet_key):
        f = Fernet(fernet_key)
        encrypted_service = f.encrypt(new_service.encode()).decode()
        encrypted_login = f.encrypt(new_login.encode()).decode()
        encrypted_password = f.encrypt(new_password.encode()).decode()


        c = DataManager.sqlite_db_connect()
        c.execute("UPDATE passwords SET service=?, login=?, password=? WHERE id=?",
                  (encrypted_service, encrypted_login, encrypted_password, record_id))
        c.connection.commit()
        edit_window.destroy()
        self.display_passwords()
        messagebox.showinfo("Успех", "Данные обновлены успешно!")

    def open_password_generator(self):
        self.master.destroy() 
        new_root = Tk()
        # Используется функция для получения размера окна
        w, h = get_window_size(new_root)
        # Устанавливается позиция в пространстве и размер
        new_root.geometry(f'500x400+{w}+{h}')
        # Создается новый объект класса PasswordGeneratorWindow, с установкой родительского окна
        window = PasswordGeneratorWindow(master=new_root)
        # Запускам mainloop(), основной цикл программы
        new_root.mainloop()


# Окно генератора паролей


class PasswordGeneratorWindow(Frame, DataManager):
    def __init__(self, master):
        super().__init__(master)
        pas = PasswordGenerator()

        self.master = master
        self.pack(fill=BOTH, expand=1)
        # конфигурация окна
        self.master.title("Генератор паролей")
        self.master.geometry("500x400")
        self.master.resizable(False, False)

        label_left = Label(self)
        label_left.pack(side=LEFT, fill=BOTH, expand=1)

        label_right = Label(self)
        label_right.pack(side=RIGHT, fill=BOTH, expand=1)

        # Виджеты левого лейбла
        service_name_label = Label(label_left, text="Введите название сервиса:")
        service_name_label.pack()

        service_name_entry = Entry(label_left)
        service_name_entry.pack()

        login_label = Label(label_left, text="Введите логин:")
        login_label.pack()

        login_entry = Entry(label_left)
        login_entry.pack()

        password_label = Label(label_left, text="Введите пароль:")
        password_label.pack()

        password_entry = Entry(label_left)
        password_entry.pack()

        save_data_button = Button(label_left, text="Сохранить данные", command=lambda: self.save_data(
            service_name_entry, login_entry, password_entry))
        save_data_button.pack()

        # Виджеты правого лейбла
        password_length_label = Label(label_right, text="Введите длину пароля:")
        password_length_label.pack()

        password_length_entry = Entry(label_right)
        password_length_entry.pack()

        password_display_label = Label(label_right, text="")
        password_display_label.pack()

        add_lowercase_checkbutton = Checkbutton(
            label_right, text="Добавить специальные символы", variable=pas.enabled_sym, command=pas.check_sym)
        add_lowercase_checkbutton.pack()

        add_uppercase_checkbutton = Checkbutton(
            label_right, text="Добавить большие буквы", variable=pas.enabled_up, command=pas.check_up)
        add_uppercase_checkbutton.pack()

        add_digits_checkbutton = Checkbutton(
            label_right, text="Добавить цифры", variable=pas.enabled_dig, command=pas.check_dig)
        add_digits_checkbutton.pack()

        generate_password_button = Button(label_right, text="Сгенерировать пароль", command=lambda: self.generate_and_display_password(
            pas, password_length_entry, generated_password_entry))
        generate_password_button.pack()

        generated_password_entry = Entry(label_right, state="readonly")
        generated_password_entry.pack()

        copy_button = Button(label_right, text="Коп.", command=lambda: self.copy_password(generated_password_entry))
        copy_button.pack()

        open_display_button = Button(self, text="Список паролей", command=self.open_display_passwords)
        open_display_button.pack(side=BOTTOM, anchor="s", padx=10, pady=10, ipadx=20)

    def copy_password(self, entry):
        entry.select_range(0, 'end')
        entry.event_generate('<<Copy>>')

    def open_display_passwords(self):
        c = DataManager.sqlite_db_connect()
        # исполняем sql запрос, выбрать все строки из таблицы паролей
        c.execute("SELECT * FROM passwords")
        # помещаем все что вернул запрос в переменную rows
        rows = c.fetchall()
        # Если в переменной rows что то есть, создаем новое окно с показом паролей
        if rows:
            # уничтожаем текущее окно
            self.master.destroy()

            new_root = Tk()
            w, h = get_window_size(new_root)
            new_root.geometry(f'500x400+{w}+{h}')
            window = DisplayPasswords(master=new_root)
            new_root.mainloop()
        # Если переменная rows пустая, соотвественно там нет ни одного пароля, показываем окно ошибки
        else:
            messagebox.showerror("Ошибка", "Нет ни одного пароля")
    # функция для генерации и отображения пароля

    def generate_and_display_password(self, password_generator, password_length_entry, generated_password_entry):
        
        password = password_generator.generate_password(password_length_entry)
        generated_password_entry.config(state=NORMAL)
        generated_password_entry.delete(0, END)
        generated_password_entry.insert(0, password)
        generated_password_entry.config(state="readonly")
    # функция для сохранения даты

    def save_data(self, service_name_entry, login_entry, password_entry):
        c = DataManager.sqlite_db_connect()
        c.execute("SELECT key FROM key")
        fernet_key = c.fetchone()[0].encode()
        # получение данных из трех полей ввода
        service_name = service_name_entry.get()
        login = login_entry.get()
        password = password_entry.get()
        if not (service_name and login and password):
            messagebox.showerror("Ошибка", "все три поля должны быть заполнены!")
            return

        f = Fernet(fernet_key)
        encrypted_service_name = f.encrypt(service_name.encode()).decode()
        encrypted_login = f.encrypt(login.encode()).decode()
        encrypted_password = f.encrypt(password.encode()).decode()

        c = DataManager.sqlite_db_connect()
        c.execute("INSERT INTO passwords(service, login, password) VALUES (?, ?, ?)",
                  (encrypted_service_name, encrypted_login, encrypted_password))
        c.connection.commit()

        messagebox.showinfo("Успешно", "Данные сохранены")


# Функция для создания мастер пароля, который испльзуется при входе в приложение
class CreateMasterPassword(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.master.resizable(False, False)

        master_password_label = Label(self, text="Введите мастер пароль:")
        master_password_label.grid(row=0, column=0)

        self.master_password_entry = Entry(self, show="*")
        self.master_password_entry.grid(row=0, column=1)

        create_password_button = Button(
            self, text="Создать пароль", command=self.create_master_password)
        create_password_button.grid(row=1, column=0, columnspan=2)


    def create_master_password(self):

        key = Fernet.generate_key()
        c = DataManager.sqlite_db_connect()
        c.execute("INSERT INTO key(key) VALUES (?)", (key.decode(),))
        c.connection.commit()

        master_password = self.master_password_entry.get()
        hashed_password = hashlib.sha256(master_password.encode()).hexdigest()
        c = DataManager.sqlite_db_connect()
        c.execute(
            "INSERT INTO master_password(master_password) VALUES (?)", (hashed_password,))
        c.connection.commit()
        self.master.destroy()

        new_root = Tk()
        w, h = get_window_size(new_root)
        new_root.geometry(f'300x200+{w}+{h}')
        window = OptionChoose(master=new_root)
        new_root.mainloop()

# Класс для проверки введенного мастер пароля
class CheckMasterPassword(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.master.resizable(False, False)

        master_password_label = Label(self, text="Введите мастер пароль:")
        master_password_label.grid(row=0, column=0)

        self.master_password_entry = Entry(self, show="*")
        self.master_password_entry.grid(row=0, column=1)

        check_password_button = Button(
            self, text="Проверить пароль", command=self.check_master_password)
        check_password_button.grid(row=1, column=0, columnspan=2)

    def check_master_password(self):
        entered_password = self.master_password_entry.get()
        hashed_password = hashlib.sha256(entered_password.encode()).hexdigest()
        c = DataManager.sqlite_db_connect()
        c.execute("SELECT master_password FROM master_password")
        saved_password = c.fetchone()[0]
        if hashed_password == saved_password:
            self.master.destroy()
            new_root = Tk()
            w, h = get_window_size(new_root)
            new_root.geometry(f'300x200+{w}+{h}')
            window = OptionChoose(master=new_root)
            new_root.mainloop()
        else:
            messagebox.showerror("Ошибка", "Неправильный мастер пароль")


class InitialClass(DataManager):
    def __init__(self):   
        db_file = 'my_database.db'
        ddl_file = 'create.ddl'



# точка входа в программу
if __name__ == '__main__':
    # если файл базы данных отсутствует, запускается создание мастер пароля и базы данных соответственно
    if not os.path.exists('my_database.db'):
        initial = InitialClass()
        # Вызываем функцию для создания базы данных
        initial.execute_ddl_file(initial.db_file, initial.ddl_file)
        root = Tk()
        w, h = get_window_size(root)
        root.geometry(f'300x200+{w}+{h}')
        master = CreateMasterPassword(master=root)
        root.mainloop()
    else:
        root = Tk()
        initial = InitialClass()
        w, h = get_window_size(root)
        root.geometry(f'300x200+{w}+{h}')
        master = CheckMasterPassword(master=root)
        root.mainloop()
