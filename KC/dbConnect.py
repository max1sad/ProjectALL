import sqlite3
import loggerS as log
from os import path,access,W_OK,R_OK
from translator import tr
#from allFunction import readFileConf

#  соединение с БД и возврат строки соеднинеия
def connectDb(path_db):
    try:
        #path_db = readFileConf('DB','path')
        print("Подключение к БД {path_d}".format(path_d=path_db))
        if path_db:
            if path.isfile(path_db) and access(path_db,W_OK) and access(path_db,R_OK):
                sqlite_connection = sqlite3.connect(path_db,check_same_thread=False,timeout=3)
            else:
                log.logM(tr("Файл БД, указанный в конфигурационном файле, не найден или недоступен") + " {f}".format(f=path_db))
                print("Файл БД, указанный в конфигурационном файле, не найден или недоступен {f}".format(f=path_db))
                quit(2)
            return sqlite_connection
        else:
            print("В конфигурационном файле не указан путь к БД")
            log.logM("В конфигурационном файле не указан путь к БД")
            quit(2)
    except sqlite3.Error as error:
        #print("Ошибка при подключении к sqlite", error)
        log.logM(tr("Ошибка подключения к БД") + " Skif: {e}".format(e=error))
        quit(2)
#sqlite_connection = connectDb()
# создание курсора для выполнения операций к БД
def createCursor(sqlite_connection):
    try:
        cursor = sqlite_connection.cursor()
        #print("База данных создана и успешно подключена к SQLite")
        log.logM(tr("Успешное подключение к БД") + " Skif")
        return cursor
    except sqlite3.Error as error:
        #print("Ошибка при подключении к sqlite", error)
        log.logM(tr("Ошибка создания курсора в")+" sqlite: {e}".format(e=error))
        quit(2)
    
#sqlite_select_query = "select * from fileInf;"
#cursor = createCursor()
# Выполнение любях sql запросов на получение данных из БД
def getSqldata(sql,cursor):
    try:
        #lock = Lock()
        #try:    
            #lock.acquire(True)
            cursor.execute(sql)
            record = cursor.fetchall()
            return record
        #finally:
        #    lock.release()
    except Exception as e:
        print("Ошибка выполнения sql запроса на получение данных: {e}".format(e=e))
        log.logM(tr("Ошибка выполнения sql запроса на получение данных") + ": {e}".format(e=e))
    #cursor.close()

#sqlite_insert_query = "INSERT INTO fileInf (name_file) VALUES (?);"
#sql_insert_param = [['/tmp/123e',],['/tmp/123e',]]
# создание записей, наверное лучеш передалть под параметры попробовать
def createData(sql,param,cursor,sqlite_connection):
    try:

        cursor.executemany(sql,param)
        #cursor.close()
        sqlite_connection.commit()
    except Exception as e:
        print("Ошибка добавления данных в БД: {e}".format(e=e))
        log.logM(tr("Ошибка добавления данных в БД") + ": {e}".format(e=e))
# удаление данных 
def delteData(sql,cursor,sqlite_connection):
    try:
        
        cursor.execute(sql)
        sqlite_connection.commit()
    except Exception as e:
        print("Ошибка удаления данных из БД: {e}".format(e=e))
        log.logM(tr("Ошибка удаления данных из БД") + ": {e}".format(e=e))
#createData(sqlite_insert_query,sql_insert_param)
#getSqldata(sqlite_select_query)
