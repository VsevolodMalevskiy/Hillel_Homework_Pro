import os
import sqlite3
from collections import Counter


def execute_query(query_sql: str):
    '''
    Функция для выполнения запроса
    :param query_sql: запрос
    :return: результат выполнения запроса
    '''
    db_pass = os.path.join(os.getcwd(), 'chinook.db')
    connection = sqlite3.connect(db_pass)
    cur = connection.cursor()
    result = cur.execute(query_sql).fetchall()
    connection.close()
    return result


# Задача 1

def calculation_sum():
    request_1 = """
      SELECT UnitPrice, Quantity
        FROM invoice_items;
    """

    rows_1 = execute_query(request_1)

    summa = 0
    for row in rows_1:
        summa += row[0] * row[1]
    print("\n#1 task")
    print(f"Общая прибыль по таблице Invoice_items = {'%.2f' % summa}\n")


def calculation_sum_sql():
    request_1_sql = """
    SELECT SUM(UnitPrice*Quantity)
      FROM invoice_items;
    """

    rows_1_sql = execute_query(request_1_sql)

    print("#1 task (SQL)")
    print(f"Общая прибыль по таблице Invoice_items = {'%.2f' % (rows_1_sql[0])}\n")


# Задача 2

def counting_duplicates():
    request_2 = """
      SELECT FirstName
        FROM customers;
    """

    rows_2 = execute_query(request_2)
    list_out = Counter(item[0] for item in rows_2)

    print("#2 task")
    for key, value in list_out.items():
        if value > 1:
            print(f"{key} {value}")


def counting_duplicates_sql():
    request_2_sql = """
      SELECT FirstName, COUNT(FirstName)
        FROM customers
        GROUP BY FirstName
        HAVING COUNT(FirstName) > 1;     
    """

    rows_2_sql = execute_query(request_2_sql)

    print("\n#2 task (SQL)")
    for item in rows_2_sql:
        print(f"{item[0]} {item[1]}")


calculation_sum()
calculation_sum_sql()
counting_duplicates()
counting_duplicates_sql()
