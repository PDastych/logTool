import sqlite3


def create_table(table_name):
    connection = sqlite3.connect('ip.db')
    cursor = connection.cursor()
    cursor.execute(f'''CREATE TABLE {table_name} (
    ip text PRIMARY KEY,
    brute_number int DEFAULT 0,
    dangerous int DEFAULT 0
    )''')
    connection.commit()
    connection.close()



def delete_table(table_name):

    connection = sqlite3.connect('ip.db')
    cursor = connection.cursor()
    cursor.execute(f'DROP TABLE {table_name}')
    connection.commit()
    connection.close()


def get_all_data(table_name):

    connection = sqlite3.connect('ip.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    array = cursor.fetchall()
    connection.commit()
    connection.close()
    return array


def get_all_ip(table_name):

    connection = sqlite3.connect('ip.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    array = cursor.fetchall()
    for i in array:
        print(f'{i[0]} - {i[1]} failed login attempts')
    connection.commit()
    connection.close()


def insert_data(table_name, array):

    connection = sqlite3.connect('ip.db')
    cursor = connection.cursor()
    cursor.executemany(f'INSERT INTO {table_name} VALUES (?,?,?)', array)
    connection.commit()
    connection.close()


def update_data(table_name, failed_array, correct_array, ban_number):
    connection = sqlite3.connect('ip.db')
    cursor = connection.cursor()
    for i in failed_array:
        cursor.execute(f'INSERT OR IGNORE INTO {table_name}(ip) VALUES(?)', (i,))
        cursor.execute(f'UPDATE {table_name} SET brute_number = brute_number + 1 WHERE ip = ?', (i,))

    for i in correct_array:
        cursor.execute(f'UPDATE {table_name} SET brute_number = brute_number -1 WHERE ip = ? and brute_number > 0', (i,))

    cursor.execute(f'UPDATE {table_name} SET dangerous = 1 WHERE brute_number >= {ban_number}')
    connection.commit()
    connection.close()


def print_ip_ranking(table_name, value):
    data = sorted(get_all_data(table_name), key=lambda x: x[1], reverse=True)
    data = data[:value]
    for idx, i in enumerate(data):
        print(f'{idx+1}. {i[0]} - {i[1]} failed login attempts')


def get_dangerous_ip(table_name):
    data = get_all_data(table_name)
    ip_list = [i[0] for i in data if i[2] == 1]
    return ip_list


def print_information_by_ip(table_name, ip):
    array = []
    try:
        connection = sqlite3.connect('ip.db')
        cursor = connection.cursor()
        for i in ip:
            cursor.execute(f"SELECT * FROM {table_name} WHERE ip='{i}'")
            array.append(cursor.fetchall())
        connection.commit()
        connection.close()
        for i in array:
            print(f'{i[0][0]} - {i[0][1]} failed login attempts')
    except:
        print('There is no such ip in database')


def delete_row_by_ip(table_name, ip_list):
    try:
        connection = sqlite3.connect('ip.db')
        cursor = connection.cursor()
        for i in ip_list:
            cursor.execute(f"DELETE FROM {table_name} WHERE ip='{i}'")
        connection.commit()
        connection.close()
    except:
        'There is no such ip in database'




