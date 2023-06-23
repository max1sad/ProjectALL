import configparser
import os
from pathlib import Path 
import loggerS as log
from translator import tr
#dirname = os.path.dirname(__file__)
#filename = os.path.join(dirname, 'skif.conf')
# чтение из файла
def read_file(path_file):
    with open(path_file) as f:
        resul = f.readlines()
    return resul
# запись в файл
def file_write(path_file,element):
    with open(path_file,'a') as f:
        f.write(element)
        f.close()
# перезапись файла
def del_file_text(path_file):
    with open(path_file,'w') as f:
        f.write("")
        f.close()
# Читаем общией конфиг, где задан блок и параметр который получить надо
def readFileConf(blok,parametr,path_conf=""):
    #dirname = read_file()
    dirname = path_conf
    #print(f"dir {dirname} {blok} {parametr}")
    if len(dirname) == 0:
        dirname = '/etc/skif.conf'
    filename= dirname
    #print(f"filen {filename}")
    config = configparser.ConfigParser()  # создаём объекта парсера
    values = ''
    if os.path.isfile(filename):
        
        try:
            config.read(filename)  # читаем конфиг
            values = config.get(blok,parametr)  # обращаемся как к обычному словарю!
                #print(values)        
        except Exception as e:
            print(e)
        if values:
            #print(f"value {values}")
            return values
        else:
            log.logM(tr("В конфигурационном файле заданы не все параметры"))
            #quit(1)
            return 0
    else:
        log.logM(tr("Конфигурационный файл не найден"))
        quit(1)
        return 0
    
# Читаем блок где указаны отслеживаемые файлы
def readFileConfControl(blok,path_conf=""): 
    #dirname = read_file()
    dirname = path_conf
    if len(dirname) == 0:
        dirname = '/etc/skif.conf'
    filename= dirname
    config = configparser.ConfigParser()  # создаём объекта парсера
    values = []
    i = 1
    if os.path.isfile(filename):
        try:
            config.read(filename)  # читаем конфиг
            while True:
                values.append(config.get(blok,str(i)))  # обращаемся как к обычному словарю!
                i += 1
                #print(values)        
        except Exception as e:
            pass
        if len(values) > 0:
            return values
        else:
            log.logM("В конфигурационном файле не заданы элементы для постановки на КЦ")
            return 0
    else:
        log.logM(tr("Конфигурационный файл не найден"))
        quit(1)
        return 0

