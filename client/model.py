import psycopg2
import pandas as pd


class DataBase:
    def __init__(self, name):
        self.name = name

    def create(self):
        connection = psycopg2.connect(port = "5432", user = "postgres", password = "1")
        cursor = connection.cursor() #здесь поменяем потом юзера
        with open("client/database_creation.sql", "r") as file:
            database_creation = file.read()
        cursor.execute(database_creation)
        connection.commit()
        cursor.execute("SELECT create_user()")
        connection.commit()
        cursor.close()
        connection.close()
        connection = psycopg2.connect(port = "5432", user = "editor", password = "1", database = "postgres")
        cursor = connection.cursor()
        cursor.execute(f"SELECT create_db('{self.name}')")
        cursor.close()
        connection.close()
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        with open("client/table_creation.sql", "r") as file:
            table_creation = file.read()
        cursor = connection.cursor()
        cursor.execute(table_creation)
        cursor.execute("SELECT create_all_tables()")
        with open("client/working.sql", "r") as file:
            sql = file.read()
        cursor.execute(sql)
        connection.commit()
        connection.commit()
        cursor.close()
        connection.close()
    
    def drop(self):
        connection = psycopg2.connect(port = "5432", user = "postgres", database = "postgres", password = "1")
        cursor = connection.cursor() #здесь поменяем потом юзера
        with open("client/database_creation.sql", "r") as file:
            database_creation = file.read()
        cursor.execute(database_creation)
        connection.commit()
        cursor.execute("SELECT create_user()")
        connection.commit()
        cursor.close()
        connection.close()
        connection = psycopg2.connect(port = "5432", user = "editor", password = "1", database = "postgres")
        cursor = connection.cursor() #здесь поменяем потом юзера
        cursor.execute(f"SELECT drop_db('{self.name}')")
        connection.commit()
        cursor.close()
        connection.close()
    
    def add_artist(self, name):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT AddArtist('{name}')")
        connection.commit()
        cursor.close()
        connection.close()
    
    def add_concert(self, artist_id, date, price, price_vip):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT AddConcert({artist_id}, '{date}', {price}, {price_vip})")
        connection.commit()
        cursor.close()
        connection.close()
    
    def add_listener(self, first_name, last_name):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT AddListener('{first_name}', '{last_name}')")
        connection.commit()
        cursor.close()
        connection.close()
    
    def add_booking(self, concert_id, listener_id, is_vip):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT AddBooking({concert_id}, '{is_vip}', {listener_id})")
        connection.commit()
        cursor.close()
        connection.close()
    
    def select_all_artists(self):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        result = cursor.execute("SELECT * FROM GetAllArtists()")
        columns = ["ID артиста", "Исполнитель", "Выручка от концертов"]
        result = cursor.fetchall()
        if len(result) == 0:
            result = pd.DataFrame(columns = columns, index = [0])
        else:
            result = pd.DataFrame(result, columns = columns)
        cursor.close()
        connection.close()
        return result
    
    def select_all_concerts(self):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM GetAllConcerts()")
        result = cursor.fetchall()
        columns = ["ID концерта", "ID исполнителя", "Дата", "Цена", "Цена VIP", "Число обычных слушателей", "Число VIP слушателей"]
        if len(result) == 0:
            result = pd.DataFrame(columns = columns, index = [0])
        else:
            result = pd.DataFrame(result, columns = columns)
        cursor.close()
        connection.close()
        return result
    
    def select_all_listeners(self):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
       
        cursor.execute("SELECT * FROM GetAllListeners()")
        result = cursor.fetchall()
        columns = ["ID слушателя", "Имя", "Фамилия"]
        if len(result) == 0:
            result = pd.DataFrame(columns = columns, index = [0])
        else:
            result = pd.DataFrame(result, columns = columns)
        
       
        cursor.close()
        connection.close()
        return result
    
    def select_all_bookings(self):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM GetAllBookings()")
        result = cursor.fetchall()
        columns = ["ID заявки", "ID концерта", "ID слушателя", "VIP"]
        if len(result) == 0:
            result = pd.DataFrame(columns = columns, index = [0])
        else:
            result = pd.DataFrame(result, columns = columns)
        cursor.close()
        connection.close()
        return result
    
    def update_artist(self, artist_id, name):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
       
        cursor.execute(f"SELECT UpdateArtist('{artist_id}', '{name}')")
        connection.commit()
        cursor.close()
        connection.close()

    def update_listener(self, listener_id, first_name, last_name):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT UpdateListener('{listener_id}, {first_name}', '{last_name}')")
        connection.commit()
        cursor.close()
        connection.close()

    def update_concert(self, concert_id, artist_id, date, price, price_vip):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT UpdateConcert({concert_id}, {artist_id}, '{date}', {price}, {price_vip})")
        connection.commit()
        cursor.close()
        connection.close()

    def update_booking(self, booking_id, concert_id, listener_id, is_vip):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
       
        cursor.execute(f"SELECT UpdateBooking({booking_id}, {concert_id}, {listener_id}, '{is_vip}')")
        connection.commit()
        cursor.close()
        connection.close()
    
    def delete_artist_by_name(self, artist_name):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT DeleteArtistByName('{artist_name}')")
        connection.commit()
        cursor.close()
        connection.close()
    
    def delete_listener_by_lastname(self, last_name):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT DeleteListenerByLastName('{last_name}')")
        connection.commit()
        cursor.close()
        connection.close()
    
    def delete_listener_by_id(self, id):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT DeleteListenerByID({id})")
        connection.commit()
        cursor.close()
        connection.close()
    
    def delete_concert(self, id):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT DeleteConcert({id})")
        connection.commit()
        cursor.close()
        connection.close()

    def delete_booking(self, id):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
       
        cursor.execute(f"SELECT DeleteBooking({id})")
        connection.commit()
        cursor.close()
        connection.close()
    
    def get_artist_by_name(self, name):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT * FROM GetArtistByName('{name}')")
        result = cursor.fetchall()
        columns = ["ID артиста", "Исполнитель", "Выручка от концертов"]
        if len(result) == 0:
            result = pd.DataFrame(columns = columns, index = [0])
        else:
            result = pd.DataFrame(result, columns = columns)
        cursor.close()
        connection.close()
        return pd.DataFrame(result)
    
    def delete_all_listeners(self):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT DeleteAllListeners()")
        connection.commit()
        cursor.close()
        connection.close()
    
    def delete_all_artists(self):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
       
        cursor.execute(f"SELECT DeleteAllArtists()")
        connection.commit()
        cursor.close()
        connection.close()
    
    def delete_all_concerts(self):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT DeleteAllConcerts()")
        connection.commit()
        cursor.close()
        connection.close()
    
    def delete_all_bookings(self):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT DeleteAllBookings()")
        connection.commit()
        cursor.close()
        connection.close()
    
    def delete_all(self):
        connection = psycopg2.connect(port = "5432", user = "editor", database = self.name, password = "1")
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT DeleteAll()")
        connection.commit()
        cursor.close()
        connection.close()

