import configparser
import os
import logger

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'bottg.conf')

def read_file(blok,parametr): 
    config = configparser.ConfigParser()  # создаём объекта парсера
    if os.path.isfile(filename):
        config.read(filename)  # читаем конфиг
        values = config[blok][parametr]  # обращаемся как к обычному словарю!
        if values:
            return values 
        else:
            logger.file_log(f"Не задан параметр в конфигурационном файле {blok} {values}")
            return 0
    else:
        logger.file_log("Конфигурационный файл не найден!!!")
        return 0



#print(read_file("CHAT","c_nabat"))
#print(read_file("DBBOT","dbname"))
#print(read_file("DBBOT","user"))
#print(read_file("DBBOT","host"))
#print(read_file("DBBOT","password"))
#print(read_file("PRODUCT","nabat"))