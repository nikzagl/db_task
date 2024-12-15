from pandastable import Table
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import *
import customtkinter
from client import model


class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.values = Variable()
        self.title("Выбор базы данных")
        app_width = 800
        app_height = 600
        x = 400
        y = 300
        self.geometry(f'{app_width}x{app_height}+{x}+{y}')
        self.my_font = customtkinter.CTkFont(family="Helvetica", size=16, weight="bold")

        menu_frame = customtkinter.CTkFrame(self, width=400, height=400, corner_radius=0)
        menu_frame.pack(side='right', expand=True, fill='both')
        menu_options_frame = customtkinter.CTkFrame(menu_frame, width=400, height=400,  corner_radius=10)
        menu_options_frame.place(relx=0.5, rely=0.5, anchor='center')

        operations_label = customtkinter.CTkLabel(master=menu_options_frame, text='Операции с базами данных', font=self.my_font)
        operations_label.pack(pady=5, padx=20)

        create_database_button = customtkinter.CTkButton(menu_options_frame, text="Создать базу данных", command=self.create_database)
        create_database_button.pack(pady=5, padx=5)

        delete_database_button = customtkinter.CTkButton(menu_options_frame, text="Удалить базу данных...", command=self.drop_database)
        delete_database_button.pack(padx=5)

        move_to_database_button = customtkinter.CTkButton(menu_options_frame, text="Перейти к базе данных...", command=self.choose_database)
        move_to_database_button.pack(pady=10, padx=5)
    
    def run(self):
       self.mainloop()
    
    def create_database(self):
        create_database_window = customtkinter.CTkToplevel(self)
        create_database_window.tilte("Создание базы данных")
        create_database_window.wm_attributes("-topmost", True)
        width = 400
        height = 150
        x = 400
        y = 300
        create_database_window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

        info_for_user = customtkinter.CTkLabel(master=create_database_window,
                                               text='Введите название для базы данных:',
                                               font=customtkinter.CTkFont(family="Helvetica", size=14))
        info_for_user.pack(side='top', pady=5, padx=20, expand=False)
        db_entry = customtkinter.CTkEntry(create_database_window)
        db_entry.pack(pady=5, padx=5)

        confirm = customtkinter.CTkButton(create_database_window, text='добавить',
                                          command=lambda: self.perform_creating_database(db_entry.get(), create_database_window))
        confirm.pack(pady=5, padx=5)
    
    def drop_database(self):
        drop_database_window = customtkinter.CTkToplevel(self)
        drop_database_window.title("Удаление базы данных")
        drop_database_window.wm_attributes("-topmost", True)
        width = 400
        height = 150
        x = 400
        y = 300
        drop_database_window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

        info_for_user = customtkinter.CTkLabel(master=drop_database_window,
                                               text='Введите название базы данных:',
                                               font=customtkinter.CTkFont(family="Helvetica", size=14))
        info_for_user.pack(side='top', pady=5, padx=20, expand=False)
        db_entry = customtkinter.CTkEntry(drop_database_window)
        db_entry.pack(pady=5, padx=5)

        confirm = customtkinter.CTkButton(drop_database_window, text='удалить',
                                          command=lambda: self.perform_dropping_database(db_entry.get(), drop_database_window))
        confirm.pack(pady=5, padx=5)

    def choose_database(self):
        choice_database_window = customtkinter.CTkToplevel(self)
        choice_database_window.title("Выбор базы данных")
        choice_database_window.wm_attributes("-topmost", True)
        width = 400
        height = 150
        x = 400
        y = 300
        choice_database_window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

        info_for_user = customtkinter.CTkLabel(master=choice_database_window,
                                               text='Введите название базы данных:',
                                               font=customtkinter.CTkFont(family="Helvetica", size=14))
        info_for_user.pack(side='top', pady=5, padx=20, expand=False)
        db_entry = customtkinter.CTkEntry(choice_database_window)
        db_entry.pack(pady=5, padx=5)

        confirm = customtkinter.CTkButton(choice_database_window, text='перейти',
                                          command=lambda: self.move_to_database(db_entry.get(), choice_database_window))
        confirm.pack(pady=5, padx=5)
    
    def move_to_database(self, database, choice_database_window):
        choice_database_window.destroy()
        choice_database_window.update()
        try:
            db = model.DataBase(database)
            df = db.select_all_artists()
        except:
            tk.messagebox.showerror("Ошибка", "Такой базы данных нет!")
            return
        width = 1050
        height = 600
        x = 400
        y = 300
        self.current_database_window = customtkinter.CTkToplevel(self)
        self.current_database_window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
        self.current_database_window.wm_attributes("-topmost", True)
        self.current_database_window.title(f"{database}")
        
        table_frame = customtkinter.CTkFrame(self.current_database_window)
        table_frame.pack(side='top', fill='both')
        self.pt = Table(table_frame, dataframe=df, editable=False)
        for col in self.pt.model.df.columns:
            self.pt.columnwidths[col] = 210
        self.pt.show()
        combobox_states = ["Исполнители", "Слушатели", "Концерты", "Заявки"]
        states_var = StringVar(value = combobox_states[0]) 
        print(database)
        combobox = customtkinter.CTkComboBox(self.current_database_window, variable=states_var, values = combobox_states, state="readonly")
        combobox.pack()
        show_table_button = customtkinter.CTkButton(self.current_database_window, text = "Показать таблицу", command = lambda: self.change_position(combobox.get(), database))
        show_table_button.pack()
        options_frame = customtkinter.CTkFrame(self.current_database_window)
        add_artist_button = customtkinter.CTkButton(options_frame, text = "Добавить исполнителя", command = lambda: self.add_artist(database, self.current_database_window))
        add_artist_button.grid(row = 1, column = 0)
        add_listener_button = customtkinter.CTkButton(options_frame, text = "Добавить слушателя", command =lambda: self.add_listener(database, self.current_database_window))
        add_listener_button.grid(row = 2, column = 0)
        add_concert_button = customtkinter.CTkButton(options_frame, text = "Добавить концерт", command= lambda: self.add_concert(database, self.current_database_window))
        add_concert_button.grid(row = 3, column = 0)
        add_booking_button = customtkinter.CTkButton(options_frame, text = "Добавить заявку", command = lambda: self.add_booking(database, self.current_database_window))
        add_booking_button.grid(row = 4, column = 0)

        update_artist_button = customtkinter.CTkButton(options_frame, text = "Обновить исполнителя", command = lambda: self.update_artist(database, self.current_database_window))
        update_artist_button.grid(row = 1, column = 1)
        update_listener_button = customtkinter.CTkButton(options_frame, text = "Обновить слушателя", command = lambda: self.update_listener(database, self.current_database_window))
        update_listener_button.grid(row = 2, column = 1)
        update_concert_button = customtkinter.CTkButton(options_frame, text = "Обновить концерт", command = lambda: self.update_concert(database, self.current_database_window))
        update_concert_button.grid(row = 3, column = 1)
        update_booking_button = customtkinter.CTkButton(options_frame, text = "Обновить заявку", command = lambda: self.update_booking(database, self.current_database_window))
        update_booking_button.grid(row = 4, column = 1)
        
        delete_artist_button = customtkinter.CTkButton(options_frame, text = "Удалить исполнителя по названию", command = lambda: self.delete_artist(database, self.current_database_window))
        delete_artist_button.grid(row = 1, column = 2)
        delete_listener_button = customtkinter.CTkButton(options_frame, text = "Удалить слушателей по фамилии", command = lambda: self.delete_listeners_by_lastname(database, self.current_database_window))
        delete_listener_button.grid(row = 2, column =2)
        delete_listenerbyid_button = customtkinter.CTkButton(options_frame, text = "Удалить слушателя по ID", command = lambda: self.delete_listener_byid(database, self.current_database_window))
        delete_listenerbyid_button.grid(row = 3, column = 2)
        delete_concert_button = customtkinter.CTkButton(options_frame, text = "Удалить концерт", command = lambda: self.delete_concert(database, self.current_database_window))
        delete_concert_button.grid(row = 4, column = 2)
        delete_booking_button = customtkinter.CTkButton(options_frame, text = "Удалить заявку", command = lambda: self.delete_booking(database, self.current_database_window))
        delete_booking_button.grid(row = 5, column = 2)
        options_frame.pack(side='right', expand=True, fill='both')

        clear_artists_button = customtkinter.CTkButton(options_frame, text = "Удалить всех исполнителей", command = lambda: self.clear_all_artists(database))
        clear_artists_button.grid(row = 1, column = 3)
        clear_listeners_button = customtkinter.CTkButton(options_frame, text = "Очистить таблицу слушателей", command = lambda: self.clear_all_listeners(database))
        clear_listeners_button.grid(row = 2, column = 3)
        clear_concerts_button = customtkinter.CTkButton(options_frame, text = "Очистить таблицу концертов", command = lambda: self.clear_all_artists(database))
        clear_concerts_button.grid(row = 3, column = 3)
        clear_bookings_button = customtkinter.CTkButton(options_frame, text = "Очистить таблицу заявок", command = lambda: self.clear_all_bookings(database))
        clear_bookings_button.grid(row = 4, column = 3)
        clear_all_button = customtkinter.CTkButton(options_frame, text = "Очистить всё", command = lambda: self.clear_all(database))
        clear_all_button.grid(row = 5, column = 3)
        options_frame.pack(side='right', expand=True, fill='both')

        search_artist_by_name_button = customtkinter.CTkButton(options_frame, text = "Найти исполнителя по названию", command = lambda: self.select_by_artist_name(database, self.current_database_window))
        search_artist_by_name_button.grid(row = 6, column = 1)
    
    def change_position(self, position, database):
        db = model.DataBase(database)
        dict_of_commands = {"Исполнители": db.select_all_artists,
                             "Слушатели": db.select_all_listeners, 
                             "Концерты": db.select_all_concerts,
                             "Заявки": db.select_all_bookings}
                             
        self.pt.model.df = dict_of_commands[position]()
        for col in self.pt.model.df.columns:
            self.pt.columnwidths[col] = 210
        self.pt.redraw()

    def get_values_from_form(self, columns, title, button_text, window):
        form = customtkinter.CTkToplevel(window)
        form.title(title)
        width = 600
        height = 200
        x = 400
        y = 300
        form.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
        form.wm_attributes("-topmost", True)
        textboxes = []
        for i, column in enumerate(columns):
            info_for_user = customtkinter.CTkLabel(master=form,
                                               text=f'{column}:',
                                               font=customtkinter.CTkFont(family="Helvetica", size=14))
            info_for_user.grid(row = i, column = 0)
            textboxes.append(customtkinter.CTkEntry(master=form, font = customtkinter.CTkFont(family="Helvetica", size=14)))
        for i in range(len(textboxes)):
            textboxes[i].grid(row = i, column = 1)
        button = customtkinter.CTkButton(form, text=button_text, command=lambda: self.values.set([textbox.get() for textbox in textboxes]))
        button.grid(row = 0, column = 2)
        button.wait_variable(self.values)
        form.destroy()
        form.update()
    
    def perform_creating_database(self, db_name, window):
        db = model.DataBase(db_name)
        db.create()
        window.destroy()
        window.update() 
    
    def perform_dropping_database(self, db_name, window):
        window.destroy()
        window.update()
        try:
            db = model.DataBase(db_name)
            db.drop()
        except Exception as e:
            print(str(e))
            tk.messagebox.showerror("Ошибка", "Такой базы данных нет либо она занята другим пользователем!")
            return
            
        
       
    def add_artist(self, db_name, window):
        db = model.DataBase(db_name)
        columns = ["Исполнитель"]
        self.get_values_from_form(columns, "Добавить исполнителя", "Добавить", window)
        db.add_artist(*self.values.get())

    def add_listener(self, db_name, window):
        db = model.DataBase(db_name)
        columns = ["Имя", "Фамилия"]
        self.get_values_from_form(columns, "Добавить слушателя", "Добавить", window)
        db.add_listener(*self.values.get())
    
    def add_concert(self, db_name, window):
        db = model.DataBase(db_name)
        columns = ["ID исполнителя", "Дата", "Цена", "Цена VIP"]
        self.get_values_from_form(columns, "Добавить концерт", "Добавить", window)
        try:
            db.add_concert(*self.values.get())
        except:
            tk.messagebox.showerror("Ошибка", "Ошибка заполнения полей", parent = window)

    def add_booking(self, db_name, window):
        db = model.DataBase(db_name)
        columns = ["ID концерта", "ID слушателя", "VIP"]
        self.get_values_from_form(columns, "Добавить исполнителя", "Добавить", window)
        try:
           db.add_booking(*self.values.get())
        except:
            tk.messagebox.showerror("Ошибка", "Ошибка заполнения полей", parent = window)
        
    def update_artist(self, db_name, window):
        db = model.DataBase(db_name)
        columns = ["ID исполнителя", "Исполнитель"]
        self.get_values_from_form(columns, "Обновить исполнителя", "Обновить", window)
        try:
            db.update_artist(*self.values.get())
        except:
            tk.messagebox.showerror("Ошибка", "Ошибка заполнения полей", parent = window)
    
    def update_listener(self, db_name, window):
        db = model.DataBase(db_name)
        columns = ["ID слушателя", "Имя", "Фамилия"]
        self.get_values_from_form(columns, "Обновить слушателя", "Обновить", window)
        try:
            db.update_listener(*self.values.get())
        except:
            tk.messagebox.showerror("Ошибка", "Ошибка заполнения полей", parent = window)
    
    def update_concert(self, db_name, window):
        db = model.DataBase(db_name)
        columns = ["ID концерта", "ID исполнителя", "Дата", "Цена", "Цена VIP"]
        self.get_values_from_form(columns, "Обновить концерт", "Обновить", window)
        try:
            db.update_concert(*self.values.get())
        except Exception as e:
            print(str(e))
            tk.messagebox.showerror("Ошибка", "Ошибка заполнения полей", parent = window)
    
    def update_booking(self, db_name, window):
        db = model.DataBase(db_name)
        columns = ["ID заявки", "ID концерта", "ID слушателя", "VIP"]
        self.get_values_from_form(columns, "Обновить концерт", "Обновить", window)
        try:
            db.update_booking(*self.values.get())
        except Exception as e:
            
            tk.messagebox.showerror("Ошибка", "Ошибка заполнения полей", parent = window)    
    
    def delete_artist(self, db_name, window):
        db = model.DataBase(db_name)
        columns = ["Исполнитель"]
        self.get_values_from_form(columns, "Удалить исполнителя по имени", "Удалить", window)
        db.delete_artist_by_name(*self.values.get())
    
    def delete_listeners_by_lastname(self, db_name, window):
        db = model.DataBase(db_name)
        columns = ["Фамилия"]
        self.get_values_from_form(columns, "Удалить слушателя по имени", "Удалить", window)
        db.delete_listener_by_lastname(*self.values.get())
    
    def delete_listener_byid(self, db_name, window):
        db = model.DataBase(db_name)
        columns = ["ID слушателя"]
        self.get_values_from_form(columns, "Удалить слушателя по ID", "Удалить", window)
        try:
            db.delete_listener_by_id(*self.values.get())
        except:
            tk.messagebox.showerror("Ошибка", "ID должно быть числом", parent = window)
    
    def delete_concert(self, db_name, window):
        db = model.DataBase(db_name)
        columns = ["ID концерта"]
        self.get_values_from_form(columns, "Удалить концерт", "Удалить", window)
        try:
            db.delete_concert(*self.values.get())
        except:
            tk.messagebox.showerror("Ошибка", "ID должно быть числом", parent = window)
    def delete_booking(self, db_name, window):
        db = model.DataBase(db_name)
        columns = ["ID заявки"]
        self.get_values_from_form(columns, "Удалить заявку", "Удалить", window)
        try:
            db.delete_booking(*self.values.get())
        except:
            tk.messagebox.showerror("Ошибка", "ID должно быть числом", parent = window)
    
    def clear_all_artists(self, db_name):
        db = model.DataBase(db_name)
        db.delete_all_artists()
    
    def clear_all_listeners(self, db_name):
        db = model.DataBase(db_name)
        db.delete_all_listeners()
    
    def clear_all_concerts(self, db_name):
        db = model.DataBase(db_name)
        db.delete_all_concerts()
    
    def clear_all_bookings(self, db_name):
        db = model.DataBase(db_name)
        db.delete_all_bookings()
    
    def clear_all(self, db_name):
        db = model.DataBase(db_name)
        db.delete_all()
    
    def select_by_artist_name(self, db_name, window):
        db = model.DataBase(db_name)
        columns = ["Исполнитель"]
        self.get_values_from_form(columns, "Выбрать исполнителя", "Выбрать", window)
        self.pt.model.df = db.get_artist_by_name(*self.values.get())
        for col in self.pt.model.df.columns:
            self.pt.columnwidths[col] = 210
        self.pt.redraw()