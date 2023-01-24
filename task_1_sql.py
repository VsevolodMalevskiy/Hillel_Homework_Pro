import os
import sqlite3

from typing import List, Set


def execute_query(query_sql: str) -> List:
    '''
    Функция для выполнения запроса
    :param query_sql: запрос
    :return: результат выполнения запроса
    '''
    db_pass = os.path.join(os.getcwd(), 'chinook.db')
    connection = sqlite3.connect(db_pass)
    cur = connection.cursor()
    result = cur.execute(query_sql)
    return result


def unwrapper(records: List) -> None:
    '''
    Функция для вывода результата выполнения запроса
    :param records: список ответа БД
    '''
    for record in records:
        print(*record)


def get_employees() -> None:
    '''
    Возвращает список
    '''
    query_sql = f'''
        SELECT *
          FROM employees
    '''
    return unwrapper(execute_query(query_sql))


# get_employees()

def get_customers(state_name=None, city_name=None) -> None:
    query_sql = '''
        SELECT FirstName
              ,City 
              ,State
          FROM customers
        '''
    filter_query = 'WHERE '
    if city_name and state_name:
        filter_query += f"City = '{city_name}' and State = '{state_name}'"
        query_sql += filter_query
    if city_name and not state_name:
        filter_query += f"City = '{city_name}'"
        query_sql += filter_query
    if state_name and not city_name:
        filter_query += f"State = '{state_name}'"
        query_sql += filter_query
    return unwrapper(execute_query(query_sql))


# get_customers(city_name='Budapest')


def get_unique_customers_by_python() -> Set:
    query_sql = f'''
        SELECT FirstName
          FROM customers
    '''
    records = execute_query(query_sql)
    result = set()
    for record in records:
        result.add(record[0])
    return result


print(len(get_unique_customers_by_python()))


def get_unique_customers_by_sql() -> List:
    query_sql = f'''
            SELECT distinct FirstName
              FROM customers
    '''
    records = execute_query(query_sql)
    result = []
    for record in records:
        result.append(record[0])
    return result