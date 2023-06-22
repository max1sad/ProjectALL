import psycopg2
from psycopg2 import OperationalError

import logger
def create_connection_bot(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print(f"Подключение к базе данных PostgreSQL прошло успешно {connection.dsn}")
        logger.file_log(f"Подключение к базе данных PostgreSQL прошло успешно {connection.dsn}")
        return connection
    except OperationalError as e:
        logger.file_log(f"Произошла ошибка '{e}'")
        quit()

def execute_read_query_bot(connection, query):
    
    result = None
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Произошла ошибка '{e}'")
        logger.file_log(f"Метод - execute_read_query_bot- {query} - '{e}'")

def add_query_update_bot(connection,list_data,query):
    #print("добавление")
    #connection.autocommit = True
    try:
        cursor = connection.cursor()
        cursor.execute(query, list_data)
        connection.commit()
    except Exception as e:
        logger.file_log(f"Метод - add_query_update_bot - {e} - {query}  {list_data}")
def delete_item_bot(connection,query):
    with connection:
        with connection.cursor() as cur:
            cur.execute(query)
            connection.commit()
#connetction = create_connection("otrs6","otrs","12345678","127.0.0.1","5432")
#select_ticket = "SELECT * from ticket;"
#id_client = '324234234'
#select_id_tg = "SELECT id FROM public.customer_user where mobile = '" + str(id_client) +"';" 
#ticket = execute_read_query(connetction,select_id_tg)
#print(len(ticket))
#if ticket:
#    print("ok")
#print(ticket[1][2])
#for tick in ticket:
#    print(tick)
#HafBN49qs4hL55hq

   