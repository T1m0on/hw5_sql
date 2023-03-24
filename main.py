import psycopg2


class Db():
    def __init__(self, database, user, password):
        self.connection = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        )
        self.cursor = self.connection.cursor()

    def init_columns(self):
        res = input('Имя столбца ') + ' ' + input('Тип столбца(например: serial primary key ')
        return res

    def create_table(self, number_of_column, name):
        create_query = """CREATE TABLE IF NOT EXISTS %s"""
        columns = ''
        count = 1
        for i in range(number_of_column):
            new_column = self.init_columns()
            if count != number_of_column:
                columns += new_column + ', '
                count += 1
            else:
                columns += new_column
        query = create_query + '(' + columns + ')'
        self.cursor.execute(query, (name,))
        self.connection.commit()
        print('Таблица успешно создана')

    def get_user_id(self,current_value, find_by):
        if find_by == 'phone_number':
            self.cursor.execute("""select * from users_phone where phone_number = %s;""",(current_value))
            user_id = self.cursor.fetchone()[0]
        else:
            self.cursor.execute("""select * from users 
            where email = %s or first_name = %s or second_name =%s;""",(current_value, current_value, current_value))
            user_id = self.cursor.fetchone()[0]
        return user_id

    def insert_user_data(self, first_name, second_name, email):
        insert_query = """INSERT INTO users(first_name, second_name, email) 
        VALUES (%s, %s, %s);"""
        self.cursor.execute(insert_query, (first_name, second_name, email))
        self.connection.commit()
        print('Пользователь добавлен')

    def insert_phone_for_user(self, email, phone_number):
        self.cursor.execute("""select * from users where email = %s;""", (email,))
        user_id = self.cursor.fetchone()[0]
        insert_query = """INSERT INTO users_phone(user_id, phone_number) VALUES(%s, %s);"""
        self.cursor.execute(insert_query, (user_id, phone_number))
        self.connection.commit()
        print('Номер успешно добавлен')

    def update_user(self, table, column, value, current_value, find_by):
        update_query = """UPDATE %s 
        SET %s = %s 
        WHERE user_id = %s;"""
        self.cursor.execute(update_query, (table, column, value, self.get_user_id(current_value, find_by)))

        self.connection.commit()
        print('Данные изменены')

    def delete_data(self, find_by, current_value):
        delete_query_user = """DELETE FROM users WHERE user_id=%s"""
        self.cursor.execute(delete_query_user, (self.get_user_id(current_value,find_by),))
        self.connection.commit()
        print('Успешно удалено')

    def delete_phone_number(self, find_by, current_value):
        delete_query_phone = f"""DELETE FROM users_phone WHERE user_id=%s"""
        self.cursor.execute(delete_query_phone, (self.get_user_id(current_value, find_by),))
        self.connection.commit()
        print('Успешно удалено')

    def select_all(self):
        select_query = """SELECT * FROM users u join users_phone up on u.user_id=up.user_id"""
        self.cursor.execute(select_query)
        print(self.cursor.fetchall())

    def find_user(self, find_by, current_value):
        select_query = """SELECT * FROM users u 
        JOIN users_phone up ON u.user_id=up.user_id 
        WHERE u.user_id=%s """
        self.cursor.execute(select_query, (self.get_user_id(current_value, find_by)))
        print(self.cursor.fetchone())

db = Db('hw_5_sql', 'postgres', 'postgres')

#TESTS

#db.create_table(4, 'users') #data for input: user_id serial primary key
                                               #first_name varchar(40)
                                               #second_name varchar(40)
                                               #email varchar(60) not null unique


#db.create_table(2, 'users_phone') #data for input:  #user_id integer references users(user_id),
                                                     #phone_number varchar(20) unique


#try:
    #db.insert_user_data('Tim', 'Prokhorov', 'prokhorovtd@ya.ru')
    #db.insert_user_data('Nas', 'Prokhorova', 'prokhorovaas@ya.ru')
    #db.insert_user_data('test1', 'test', 'aaa')

    #db.insert_phone_for_user('prokhorovaas@ya.ru', '79680202547')
    #db.insert_phone_for_user('prokhorovtd@ya.ru', '79680202546')
    #db.insert_phone_for_user('prokhorovtd@ya.ru',  '79295664178')
    #db.insert_phone_for_user('aaa',  '1231241')

    #db.update_user('users', 'first_name', 'Timon', 'prokhorovtd@ya.ru', 'email')

    #db.delete_phone_number('email', 'prokhorovtd@ya.ru')
    #db.delete_data('email', 'aaa')
    #db.find_user('email', 'prokhorovtd@ya.ru')
    #db.cursor.execute('drop table users_phone;')
    #db.cursor.execute('drop table users;')

#except Exception as ex:
    #print(ex)