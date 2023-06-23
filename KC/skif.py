#!/usr/bin/python3
from sys import argv
from os import path
from mainSkif import  getDublecate,analysisOfNumbering,addElements,getHelp,readConfParam,checkDBFile,getElementDefaultConf,getElementDefaultDB,conAllDataBase,checkKC, trackedItems,checkHashSumConfFile,deleteALLDb
from translator import tr
from loggerS import logM

# Переменные для выбора параметров.
par_u = 'false'
par_p = 'false'
par_p_path = ''
par_I = 'false'
par_I_number = ''
par_i = 'false'
par_i_number = ''
par_n = 'false'
par_n_number = ''
par_s = 'false'
par_t = 'false'
par_a = 'false'
par_a_path = ''
par_t_number = ''
par_d = 'false'
par_r = 'false'
lenght = len(argv)

# считаем что указали параметр. 
if lenght > 1:
    i = 1
    while i < lenght:
        if argv[i] == '-h' or argv[i] == '--help':
            getHelp()
            quit()
        if argv[i] == '-u':
            par_u = 'true'
            #break
        if argv[i] == '-t':
            if lenght > i+1:
                print("ok")
                if argv[i+1].isdigit():
                    #print(f"-I {argv[i+1]}")
                    par_t = 'true'
                    par_t_number = argv[i+1]
                else:
                    print("Опция -t должна содержать только цифры")
                    quit()
            else:
                print("Параметр задан неверно")
                quit()
        if argv[i] == '-s':
            par_s = 'true'
        if argv[i] == '-d':
            par_d = 'true'
        if argv[i] == '-r':
            par_r = 'true'
        if argv[i] == '-p':
            if lenght > i+1:
                #print("{p}/skif.conf".format(p=argv[i+1]))
                if path.isfile(argv[i+1]):
                    #print(f"-p {argv[i+1]}")
                    par_p = 'true'
                    par_p_path = argv[i+1]
                    #file_write(par_p_path)
                else:
                    print("Не наден конфигурационный файл, указанный в качестве аргумента для опции -p")
                    quit()
            else:
                print("Параметр задан неверно")
                quit()
        if argv[i] == '-a':
            if lenght > i+1:
                #print("{p}/skif.conf".format(p=argv[i+1]))
                if path.isfile(argv[i+1]):
                    #print(f"-p {argv[i+1]}")
                    par_a = 'true'
                    par_a_path = argv[i+1]
                    #file_write(par_p_path)
                else:
                    print("Не наден файл, указанный в качестве аргумента для опции -a")
                    quit()
            else:
                print("Параметр задан неверно")
                quit()
        if argv[i] == '-I':
            if lenght > i+1:
                if argv[i+1].isdigit():
                    #print(f"-I {argv[i+1]}")
                    par_I = 'true'
                    par_I_number = argv[i+1]
                else:
                    print("Опция -I должна содержать только цифры")
                    quit()
            else:
                print("Параметр задан неверно")
                quit()
        if argv[i] == '-i':
            if lenght > i+1:
                if argv[i+1].isdigit():
                    #print(f"-I {argv[i+1]}")
                    #conAllDataBase()
                    par_i = 'true'
                    par_i_number = argv[i+1]
                    
                else:
                    print("Опция -i должна содержать только цифры")
                    quit()
            else:
                print("Параметр задан неверно")
                quit()
        if argv[i] == '-n':
            if lenght > i+1:
                if argv[i+1].isdigit():
                    #print(f"-I {argv[i+1]}")
                    #conAllDataBase()
                    par_n = 'true'
                    par_n_number = argv[i+1]
                    
                else:
                    print("Опция -n должна содержать только цифры")
                    quit()
            else:
                print("Параметр задан неверно")
                quit()
        i += 1
# Вызов определение параметров, которые могут быть совместно указаны
def addElementsDB():
    print("Постановка объектов на КЦ")
    logM(tr("Постановка объектов на КЦ"))
    analysisOfNumbering(path_conf=par_p_path)
    readConfParam(update_kc="update")
    conAllDataBase()
    deleteALLDb()
    checkHashSumConfFile("createHs")
    checkKC(time_lim=par_t_number)
    quit()
#Удаление и запись новых элементов в конфигурационный файл
if par_a == 'true' and par_r == 'true':
    #print("Удаление элементов конфигурационного файла и запись новых элементов из файла: {f}".format(f=par_a_path))
    #logM("{txt}: {f}".format(txt=tr("Удаление элементов конфигурационного файла и запись новых элементов из файла"),f=par_a_path))
    analysisOfNumbering(path_conf=par_p_path,del_elements="DEL")
    addElements(par_a_path,path_conf=par_p_path)
    quit()
#Добавление элементов в конфигурационный файл
if par_a == 'true' and par_r == 'false':
    #print(par_a_path)
    addElements(par_a_path,path_conf=par_p_path)
    quit()
# Проверка дубликатов в БД по файлам и по типу отслеживания 
if par_d == 'true':
    readConfParam(par_p_path)
    conAllDataBase()
    getDublecate()
    quit()
# Запуск на проверку КЦ с новым конфигурационным файлом
if par_p == 'true' and par_u == 'false' and par_i == 'false' and par_I == 'false' and par_n == 'false' and par_s == 'false':
    print("Запуск проверки КЦ с новым конфигурационным файлом")
    readConfParam(par_p_path)
    conAllDataBase()
    checkHashSumConfFile("checkHs",path_conf=par_p_path)
    trackedItems(time_lim=par_t_number)
    quit()
# Постановка объектов на КЦ с новым конфигурационным файлом
if par_p == 'true' and par_u == 'true' and par_i == 'false' and par_I == 'false' and par_n == 'false' and par_s == 'false':
    print("Постановка объектов на КЦ с новым конфигурационным файлом {pat}".format(pat=par_p_path))
    logM(tr("Постановка объектов на КЦ с новым конфигурационным файлом") + " {pat}".format(pat=par_p_path))
    analysisOfNumbering(path_conf=par_p_path)
    readConfParam(par_p_path,update_kc="update")
    conAllDataBase()
    deleteALLDb()
    checkHashSumConfFile("createHs",path_conf=par_p_path)
    checkKC(time_lim=par_t_number)
    quit()
# Постояновко объектов на КЦ с дефолтным конфигурационным файлом
if par_u == 'true' and par_p == 'false' and par_i == 'false' and par_I == 'false' and par_s == 'false':
    addElementsDB()
# Печать на консоль элементов из конфигурационного файла
if par_I == 'true' and par_u == 'false':
     readConfParam(par_p_path)
     conAllDataBase()
     getElementDefaultConf(par_I_number=par_I_number,path_new=par_p_path,time_lim=par_t_number)
     quit()
# Печать на консоль элементов стоящих на КЦ в БД
if par_i == 'true' and par_u == 'false':
     readConfParam(par_p_path)
     conAllDataBase()
     getElementDefaultDB(par_i_number=par_i_number)
     quit()
# Проверка КЦ по одному объекту из БД
if par_n == 'true' and par_u == 'false' and par_s == 'false':
    print("Запуск проверки КЦ указанного элемента")
    readConfParam(par_p_path)
    conAllDataBase()
    checkHashSumConfFile("checkHs",path_conf=par_p_path)
    trackedItems(number_obj=par_n_number,time_lim=par_t_number)
    quit()
# Отчет в консольном варианте без таблицы по одному элементу
if par_n == 'true' and par_u == 'false' and par_s == 'true':
    print("Запуск проверки КЦ указанного элемента")
    readConfParam(par_p_path)
    conAllDataBase()
    checkHashSumConfFile("checkHs",path_conf=par_p_path)
    trackedItems(number_obj=par_n_number,type_otchet='console',time_lim=par_t_number)
    quit()
# Отчет в консольном варианте по всем элементам
if par_s == 'true' and par_u == 'false':
    print("Запуск проверки КЦ всех элементов")
    readConfParam(par_p_path)
    conAllDataBase()
    if checkDBFile() == 1:
        checkHashSumConfFile("checkHs",path_conf=par_p_path)
        trackedItems(type_otchet='console',time_lim=par_t_number)
    else:
        addElementsDB()
    quit()

# Проверка параметров запуска скрипта
# Не указали параметров запуска, тогда предполагаем что запустили просто на проверку KC
if lenght == 1 or par_t == "true":
    print("Запуск проверки КЦ всех элементов")
    analysisOfNumbering(path_conf=par_p_path)
    readConfParam()
    conAllDataBase()
    if checkDBFile() == 1:
        checkHashSumConfFile("checkHs")
        trackedItems(time_lim=par_t_number)
        quit()
    else:
        addElementsDB()
getHelp()    
