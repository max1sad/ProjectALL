import parcerStr
from allFunction import readFileConf, readFileConfControl,read_file,file_write,del_file_text
import fileAction as af
import hashSum
import loggerS as log
from prettytable import PrettyTable
from itertools import groupby
from os import access,R_OK,W_OK
import threading
#from time import sleep, perf_counter
import time
from threading import Thread
import dbProvide as db
from math import ceil
from translator import tr
from pathlib import Path 
from re import match
#from progress.bar import Bar
# Массив для формирования отчета
mytable_file = PrettyTable()
mytable_str = PrettyTable()
mytable_catalog = PrettyTable()

# добавление списка строк
#mytable_file.field_names = ["Файл","Тип КЦ", "Состояние", "Хэш сумма"]
mytable_file.field_names = ["Файл", "Состояние"]
#mytable_str.field_names = ["Файл","Тип КЦ", "№ Строки","Состояние", "Хэш сумма"]
mytable_str.field_names = ["Файл","№ Строки","Состояние"]
#mytable_catalog.field_names = ["Файл","Тип КЦ","Состояние","Хэш сумма"]
mytable_catalog.field_names = ["Каталог","Состояние"]
arr_repo_file = []
arr_repo_str = []
arr_repo_catal = []
otchet_f_str = []
otchet_d_cat = []
time_limit = ''
global_conf = ""
path_db = ''
arr_controll_summ = ''
max_threading = ''
max_count_elements = ''
glob_param = ''
# справка по параметрам
def getHelp():
    mytable_help = PrettyTable()
    mytable_help.field_names = ['Опция','Описание']
    print("Программа skif предназначена для котроля целостности объектов файловой системы")
    
    print("Используемые понятия:\n \
\tОбъект — объект проверки (файл, строка)\n \
\tЭлемент (правило) — объект проверки или их совокупность, указанная в конфигурационном файле\n")

    arr_help = [['-p','Запуск программу на проврку КЦ с указанием нового конфигурационного файла (с указанием имени файла.)'],
                ['-u','Инициализация БД данными для постановки объектов на контроль целостности'],
                ['-I','Раскрытие переченя объектов контроля для указанного номера элемента из конфигурационного файла (пример: -I 1)'],
                ['-i','Раскрытие переченя объектов контроля для указанного номера элемента из БД (пример: -i 1)'],
                ['-s','Сокращенный формат вывода информации на консоль, удобный для дальнейшей обработки'],
                ['-n','Произвести контроль КЦ только для отдельного, указанного в опции правила'],
                ['-a','Добавление элементов в конфигурационный файл из указанного файла (пример: -a /tmp/elements.txt)'],
                ['-d','Проверка элементов на дубликаты файлов в БД с учетом типа постановки на КЦ'],
                ['-r','Удаление элементов конфигурационого файла (примечание: запускать с ключем -a)']
                ]

    #['-t','Установить ограничение времени расчета контрольной суммы для одного файла в секундах (пример: -t 30)']
    i = 0
    while i < len(arr_help):
        mytable_help.add_row(arr_help[i])
        i += 1
    mytable_help.border = False
    mytable_help.align = "l"
    print(mytable_help)
    print("Возможные поведения программы:")
    print("\t1) При запуске с ключом -u, если при чтении конфигурационного файла обнаружатся повторяющиеся элементы, тогда прекращается работы программы\n \
\tт.к. это может привезти к большому количеству дубликатов.\n \
\tПри добавлении в конфигурационный файл элементов, если находит повторяющийся элемент в конфигурационном файле, то такой элемент пропускается(если находит\n \
\tдубликаты в файле и в конфигурационном файле, тогда берутся индивидуальные элементы).")
# получение дубликатов из БД
def getDublecate():
    dublicate = []
    dublicate = db.getFileDublicate()
    if len(dublicate) > 0:
        i = 0
        while i < len(dublicate):
            print("В БД имеются повторяющиеся объекты в правилах:{d1}, {d2}".format(d1=dublicate[i][0],d2=dublicate[i+1][0]))
            i += 2
    else:
        print("Дублирующих файлов в БД skif не найдено.")
# Анализ нумерации в конфигурациноом файле.
def analysisOfNumbering (path_conf="",del_elements=""):
    arr_numeration = []
    dirname = path_conf
    if len(dirname) == 0:
        dirname = '/etc/skif.conf'
    filename= dirname
    if access(filename,R_OK) and access(filename,W_OK):
        all_conf = read_file(filename)
        try:
            i = all_conf.index("[RULES]\n")
            i += 1
        except Exception as e:
            print("Не удалось найти блок [RULES] в конфигурационном файле.")
            quit(1)
        if del_elements == "DEL":
            while True:
                if i < len(all_conf): 
                    resul = match('^[0-9]+=',all_conf[i])
                    if resul:
                        #
                        del all_conf[i]
                        i -= 1
                    i += 1
                else:
                    break
        else:
            while i < len(all_conf):
                resul = match('^[0-9]+=',all_conf[i])
                #print(all_conf[i])
                if resul:
                    
                    n = resul.group()
                    #print(n[:-1])
                    arr_numeration.append(int(n[:-1]))
                i += 1
        if len(arr_numeration) > 0:
            arr_numeration.sort()
            #sorted(arr_numeration)
            i = 0
            while i < len(arr_numeration):
                if int(arr_numeration[i]) != i+1:
                    print("Конфигурационный файл в блоке [RULES] имеет неверную нумерацию.")
                    quit(1)
                i += 1
        
            return arr_numeration
        else:
            if del_elements == "DEL":
                del_file_text(filename)
                for el in all_conf:
                    file_write(filename,el)
                #print(all_conf)
            else:
                return 0
    else:
        print("Недостаточно прав для чтения конфигурационного файла: {}".format(f=filename))
        quit(1)
# поиск повторяющихся в конфигурационном файле
def repetitionOfElements(arr_el_conf):
    if arr_el_conf == 0:
        return []
    else:
        dup = [x for i, x in enumerate(arr_el_conf) if x in arr_el_conf[:i]]
        return dup

#Добавление элементов в конфигурационный файл на вход подается путь до конфигурационного файла
def addElements(path_file,path_conf=""):
    arr_file = []
    dirname = path_conf
    if len(dirname) == 0:
        dirname = '/etc/skif.conf'
    filename= dirname
    if access(filename,R_OK) and access(filename,W_OK):
        if access(path_file,R_OK):
            arr_number = analysisOfNumbering(path_conf)
            arr_file = read_file(path_file)
            arr_file_u = []
            if len(arr_file) > 0:
                dubl = repetitionOfElements(arr_file)
                if dubl:
                    print("В файле содержатся повторяющиеся элементы:{p}".format(p="  ".join(dubl)))
                arr_file_u = list(set(arr_file))
            if arr_number == 0:
                last_number = 1
                if len(arr_file_u) > 0:
                    for el in arr_file_u:
                        file_write(filename,"\n{last_n}={e}".format(last_n=last_number,e=el.strip()))
                        last_number += 1
            else:
                last_number = int(arr_number[-1]) + 1
                arr_controll_summ = readFileConfControl("RULES",path_conf)
                dubl = repetitionOfElements(arr_controll_summ)
                arr_unique_el = []
                if dubl:
                    print("В конфигурационном файле содержатся повторяющиеся элементы:{p}".format(p="  ".join(dubl)))
                arr_unique_el = list(set(arr_controll_summ))
                if len(arr_file_u) > 0:
                    for el in arr_file_u:
                        try:   
                            index_el = arr_unique_el.index(el.strip())
                            print("Данный элемент уже имеется в конфигурационном файле и не будет добавлен: {p}".format(p=el))
                        except Exception:
                            file_write(filename,"\n{last_n}={e}".format(last_n=last_number,e=el.strip()))
                            last_number += 1
        else:
            print("Не удалось прочитать файл: {f}".format(f=path_file))
            quit(1)
    else:
        print("Недостаточно прав для чтения или записи в конфигурационный файл: {f}".format(f=filename))
        quit(1)

def readConfParam(path="",update_kc=""):
    global path_db
    global arr_controll_summ
    global max_threading
    global max_count_elements
    global glob_param
    
    path_db = readFileConf('DB','path',path) 
    max_threading = int(readFileConf('SETTING','max_threading',path))
    max_count_elements = readFileConf('SETTING','count_object',path)
    glob_param = readFileConf('GLOBAL','glob',path)
    if len(update_kc) > 3:
        analysisOfNumbering(path)
        arr_controll_summ = readFileConfControl("RULES",path)
        if  arr_controll_summ == 0 :
            print("Не заданы элементы для постановки на КЦ в конфигурационном файле")
            log.logM(tr("Не заданы элементы для постановки на КЦ в конфигурационном файле"))
            quit(1)
    
def conAllDataBase():
    global global_conf
    #print(f"path_conf {path_db}")
    #path_db = readFileConf('DB','path',path_db)
    
    db.connectDataBase(path_db)
    gl_p = db.getGlobalParam()
    if len(gl_p) > 0:
        global_conf = gl_p[0][0]
# Очиста БД перед загрузкой новых объектов на КЦ
def deleteALLDb():
    # временно делаю постоянно удаление перед запуском
    db.deleteTableAllData('fileInf')
    db.deleteTableAllData('md5sum_file')
    db.deleteTableAllData('parameters')
    db.deleteTableAllData('global_param')
# Проверка поставлены на КЦ объекты
def checkKC(time_lim):
    global time_limit
    time_limit = time_lim
    if db.getCoutnFileInf()[0][0] != 0: 
        dubl = repetitionOfElements(arr_controll_summ)
        if dubl:
            print("В конфигурационном файле содержатся повторяющиеся элементы:{p}".format(p="  ".join(dubl)))
            quit(1)
        # заполнение элементов из конфига в БД
        createElementDB()
        getDublecate()
    else:
        print('БД не очищена, дальнейшая работа программы невозможна.')
        quit(2)
# проверка наличия данных в БД
def checkDBFile():
    if db.getCoutnFileInf()[0][0] > 0:
        return 1
    else:
        return 0
# Раскрытие объектов по элементно, без дальнейшей записи и анализа из объектов уже стоящих на КЦ
def getElementDefaultDB(par_i_number):
                    pravilo_is_id = getPraviloIsDb(par_i_number)
                    #print(pravilo_is_id)
                    
                    if pravilo_is_id != 0:
                        #information = getFilesByCriteria(pravilo_is_id[0][0].split(';'))
                        information = db.getFile(pravilo_is_id[0][2])
                        #print("information", information)
                        #quit()
                        if information != 0:
                            i = 0
                            print("Перечень объектов контроля для указанного номера элемента из БД: {pr}".format(pr=pravilo_is_id[0][0]))
                            
                            if pravilo_is_id[0][1] == 'l':
                                first_elem = information[0][0]
                                print("Файл: {inf}".format(inf=information[0][0])) 
                                j = 1
                                while j < len(information):
                                    if information[j][0] != first_elem:
                                        print("Файл: {inf}".format(inf=information[j][0]))
                                        first_elem = information[j][0]
                                    j += 1
                                quit()
                            else:
                                while i < len(information):
                                    print("Файл: {inf}".format(inf=information[i][0]))
                                    i += 1
                                quit()
                        else:
                            print("По заданному правилу {pr} не удалось найти объекты постановки на КЦ".format(pr=pravilo_is_id))
                    else:
                        print("В БД нет правила с указанным номером правила: {par_n}".format(par_n=par_i_number))
                        quit()
# Раскрытие объектов по элементно, без дальнейшей записи и анализа из конфигурационного файла
def getElementDefaultConf(par_I_number,path_new="",time_lim=""):
                    #conAllDataBase()
                    global global_conf
                    global time_limit
                    time_limit = time_lim
                    pravilo_is_id = readFileConf('RULES',par_I_number,path_new)
                    if glob_param:
                        
                        global_conf = glob_param
                    else:
                        global_conf = 'NULL'
                    if pravilo_is_id != 0:
                        arr_pravilo = pravilo_is_id.split(';')
                        information = getFilesByCriteria(arr_pravilo)

                        #print("information",information)
                        if information != 0 and information != 3:
                            i = 0
                            print("Перечень объектов контроля для указанного номера элемента из конфигурационного файла: {pr}".format(pr=pravilo_is_id))
                            if len(arr_pravilo) >= 2 and arr_pravilo[1] == 'l':
                                first_elem = information[0][0]
                                print("Файл: {inf}".format(inf=information[0][0])) 
                                j = 1
                                while j < len(information):
                                    if information[j][0] != first_elem:
                                        print("Файл: {inf}".format(inf=information[j][0]))
                                        first_elem = information[j][0]
                                    j += 1
                                #quit()
                            else:    
                                while i < len(information):
                                    #if information[i][2] == 'OK':
                                    print("Файл: {inf}".format(inf=information[i][0]))
                                    #else:
                                    #    print("Если указали каталог, то он должен бытьс параметром d")
                                    i += 1
                            quit()
                        else:
                            if information == 3:
                                print("Каталог на КЦ не содержит объектов в правиле: {pr}".format(pr=pravilo_is_id))
                            else:
                                print("По заданному правилу {pr} не удалось найти объекты постановки на КЦ".format(pr=pravilo_is_id))
                    quit()
# Функция раскрытия строки параметров, т.е. на вход подается строка с путем, дальше происходит раскрытие ее, и возврат значений.
## получить файлы по критерию
def getFilesByCriteria(arr_all_file):
        i = 0
        type_obj = ''
        resul_h = [] 
        arr_vr = []
        type_p = ''
        # Проверяем существует ли каталог или файл(предполагаем что не содежит регулярного выражения)
        if parcerStr.checkFileOrCatalog(arr_all_file[0]) == 1:
            type_obj = 'catal'
            arr_vr.append(arr_all_file[0])
        if parcerStr.checkFileOrCatalog(arr_all_file[0]) == 2:
            type_obj = 'file'
            arr_vr.append(arr_all_file[0])
        
        #print("type", type_obj)
        # Полный путь
        path_all = arr_all_file[0]
        # проверяем путь указана напрямую к файлу который существует или там содержатся дополнительные параметры (d,f,l,(All))
        if len(arr_all_file) > 1:
            # получаем тип проверки (d,f,l)
            type_p = arr_all_file[1]
            
            # смотрим если указан тип проверка (f)
            if type_p == 'f':
                # смотрим на существованием элемента без раскрытия регулярки
                if len(type_obj) == 0:
                    i = 0 
                    arr_yes_f = []  
                    # Раскрываем регулярку, получаем массив обьектов 
                    res = af.regexObj(path_all,type_p,global_conf=global_conf)
                    #print(res)
                    while i < len(res):
                        # если возвращаемый путь к каталогу и часть с регулярныйм выражением существуют
                        if parcerStr.checkFileOrCatalog(res[i]+"/"+path_all.rpartition('/')[2]) == 2:
                            arr_yes_f.append(res[i]+"/"+path_all.rpartition('/')[2])
                        i += 1
                    # Смотрим что массив не пустой, тогда вызвваем подсчет хэш суммы, иначе вызываем метод поиска файлов по регулярному выражению.
                    if len(arr_yes_f) > 0:
                        resul_h = hashSum.hashFileAll(arr_yes_f,time_lim=time_limit,max_threading=max_threading)
                    else:
                        resul_h = hashSum.hashFileAll(sum(af.glob_re(res,path_all.rpartition('/')[2],count_obj_yes=max_count_elements,global_conf=global_conf), []),time_lim=time_limit,max_threading=max_threading)
                        #print(f"{resul_h}  \n  {path_all.rpartition('/')[2]}")
                    #if len(resul_h) > 0:
                    #    db.createFile(resul_h,type_p,pravilo)
                else:
                    if type_obj == "file":
                        resul = af.checkFileRegGlobal(arr_vr[0],global_conf=global_conf)
                        resul_h = hashSum.hashFileAll(resul,time_lim=time_limit,max_threading=max_threading)
            #  если указан тип проверки (l)
            if type_p == 'l':
                # смотрим на существованием элемента без раскрытия регулярки
                if len(type_obj) == 0:
                    i = 0 
                    arr_yes_f = []  
                    # Раскрываем регулярку, получаем массив обьектов 
                    res = af.regexObj(path_all,'f',global_conf=global_conf)
                    #print(res)
                    
                    while i < len(res):
                        # если возвращаемый путь к каталогу и часть с регулярныйм выражением существуют
                        if parcerStr.checkFileOrCatalog(res[i]+"/"+path_all.rpartition('/')[2]) == 2:
                            arr_yes_f.append(res[i]+"/"+path_all.rpartition('/')[2])
                        i += 1
                    # Смотрим что массив не пустой, тогда вызвваем подсчет хэш суммы, иначе вызываем метод поиска файлов по регулярному выражению.
                    if len(arr_yes_f) > 0:
                        resul_h = hashSum.hashFileReadLine(arr_yes_f,action_t="str_ok",time_lim=time_limit)
                        #print("re",resul_h)
                    else:
                        resul_h = hashSum.hashFileReadLine(sum(af.glob_re(res,path_all.rpartition('/')[2],count_obj_yes=max_count_elements,global_conf=global_conf), []),action_t="str_ok",time_lim=time_limit)
                    #if len(resul_h) > 0:
                    #    print(resul_h)
                    #    db.createFile(resul_h,type_p,pravilo)
                else: 
                    if type_obj == "file":
                        resul = af.checkFileRegGlobal(arr_vr[0],global_conf=global_conf)
                        resul_h = hashSum.hashFileReadLine(resul,action_t="str_ok",time_lim=time_limit)
            if type_p  == 'd':
                # смотрим на существованием элемента без раскрытия регулярки
                if len(type_obj) == 0:
                    # Раскрываем регулярку, получаем массив обьектов
                    res = af.regexObj(path_all,'d',global_conf=global_conf)
                    #print("res",res)
                    # проверяем указан ли 3 параметр, отвечающий за глуюину раскрытия
                    if len(arr_all_file) >= 3 and arr_all_file[2] == 'ALL':
                        #print(res)
                        resul = sum(af.glob_re(res,glob_mask="**/*",count_obj_yes=max_count_elements,global_conf=global_conf), [])
                            
                        #print(resul)
                        #quit()
                    else: 
                        # получаем все файлы в каталоге в котром отслеживать нужно
                        resul = af.allDir(res,'f',global_conf=global_conf)
                    #print(f"resul--- {resul}")
                    if len(resul) > 0:
                        resul_h = hashSum.hashFileAll(resul,time_lim=time_limit,max_threading=max_threading)
                        #db.createFile(resul_h,type_p,pravilo)
                    #else: 
                        #log.logM(f"Найти объекты отслеживания не удалось {';'.join(arr_all_file[i])}")
                    #    print(f"Найти объект отслеживания не удалось {';'.join(arr_all_file[i])}")  
                else:
                    # проверяем указан ли 3 параметр, отвечающий за глуюину раскрытия
                    if len(arr_all_file) >= 3 and arr_all_file[2] == 'ALL':
                        resul = sum(af.glob_re(arr_vr,glob_mask="**/*",count_obj_yes=max_count_elements,global_conf=global_conf), [])
                        
                    else:
                        # получаем все файлы в каталоге в котром отслеживать нужно
                        resul = af.allDir(arr_vr,'f',global_conf=global_conf)
                        #print(resul)
                    if len(resul) > 0:
                        resul_h = hashSum.hashFileAll(resul,time_lim=time_limit,max_threading=max_threading)
                        #print(resul_h)
                        #db.createFile(resul_h,type_p,pravilo)
                    else: 
                        if access(arr_all_file[i], R_OK):
                            #log.logM(f"Найти объекты отслеживания не удалось {';'.join(arr_all_file[i])}")
                            if type_p != 'd':
                                print("Найти объект отслеживания не удалось {obj}".format(obj=arr_all_file[i])) 
                        else:
                             print("Отказано в доступе {file}".format(file=arr_all_file[i]))
                             #log(tr("Отказано в доступе") + " {file}".format(file=arr_all_file[i]))  
        else:
            # смотрим на существованием элемента без раскрытия регулярки
            #print("path_all", path_all)
            if len(type_obj) == 0:
                i = 0 
                arr_yes_f = []  
                # Раскрываем регулярку, получаем массив обьектов 
                res = af.regexObj(path_all,'f',global_conf=global_conf)
                #print(f"res  {res}")
                while i < len(res):
                    # если возвращаемый путь к каталогу и часть с регулярныйм выражением существуют
                    if parcerStr.checkFileOrCatalog(res[i]+"/"+path_all.rpartition('/')[2]) == 2:
                        arr_yes_f.append(res[i]+"/"+path_all.rpartition('/')[2])
                    i += 1
                # Смотрим что массив не пустой, тогда вызвваем подсчет хэш суммы, иначе вызываем метод поиска файлов по регулярному выражению.
                if len(arr_yes_f) > 0:
                    resul_h = hashSum.hashFileAll(arr_yes_f,time_lim=time_limit,max_threading=max_threading)
                else:
                    resul_h = hashSum.hashFileAll(sum(af.glob_re(res,path_all.rpartition('/')[2],count_obj_yes=max_count_elements,global_conf=global_conf), []),time_lim=time_limit,max_threading=max_threading)
                    #if len(resul_h) > 0:
                    #    db.createFile(resul_h,type_p,pravilo)
            else:
                if type_obj == 'file':
                    resul = af.checkFileRegGlobal(arr_vr[0],global_conf=global_conf)
                    #print("sdf",resul)
                    resul_h = hashSum.hashFileAll(resul,time_lim=time_limit,max_threading=max_threading)
                    #print(resul_h)
                #else:
                #    print(f"Правило без параметра может содержать только файлы.")
                #print(arr_vr)
        if len(resul_h) > 0:
            return resul_h
        else:
            if type_p != 'd':
                return 0
            else:
                if type_obj == 'catal' or len(res) > 0:
                    return 3
                else:
                    return 0
# Функция постановки и отслеживания Конфигурационного файла на КЦ, принимает 1-2 параметра, тип контроля (Хэш сумма, постановка на контроль)
def checkHashSumConfFile(type_control,path_conf=""):
    dirname = path_conf
    if len(dirname) == 0:
        dirname = '/etc/skif.conf'
    pravilo= dirname
    
    if type_control == 'createHs':
        #print(f"pravilo {pravilo}")
        resul_hs_conf = hashSum.hashFileAll([pravilo],time_lim=time_limit,max_threading=max_threading)
        #print(resul_hs_conf)
        db.createFile(resul_hs_conf,'f',pravilo,'conf')
    if type_control == 'checkHs':
        if db.getCoutnFileInf()[0][0] > 0:
            hash_sum_tek = hashSum.hashFileAll([pravilo],time_lim=time_limit,max_threading=max_threading)
            id_conf = db.getParameters(pravilo)
            #print("id_conf ",id_conf)
            if len(id_conf) > 0:
                inf_conf = db.getElementData(id_conf[0][0])
                if len(inf_conf) > 0:
                    #print(inf_conf[0][1],hash_sum_tek[0][1])
                    if inf_conf[0][1] != hash_sum_tek[0][1]:
                        print("Хэш сумма конфигурационного файла skif была изменена. Для повторной инициализации БД данными для постановки объектов на контроль целостности необходимо запустить программу с опцией -u")
                        log.logM(tr("Хэш сумма конфигурационного файла skif была изменена. Для повторной инициализации БД данными для постановки объектов на контроль целостности необходимо запустить программу с опцией -u"))
            else:
                print("В БД не найдена запись с указанным именем конфигурационного файла программы.")
        else:
            print("В БД не найдены объекты для проверки КЦ")
            log.logM(tr("В БД не найдены объекты для проверки КЦ"))
            #quit()     

# получаем правило из БД, по указанному номеру правила, с которым ранее было считано с конфига
def getPraviloIsDb(number):
    all_prav = db.getParametersNum(number)
    #print(all_prav)
    #quit()
    if len(all_prav) > 0:
        return all_prav
    else:
        return 0        
# Функция добавления записей в БД из прочтенного конфига, так же сделать дозапись параметров в БД,передавать отдельным параметром
def createElementDB():
    #readFileConfControl("RULES")
    arr_all_file = parcerStr.parcerStrFile(arr_controll_summ)
    #print(arr_all_file)
    #glob_param = readFileConf('GLOBAL','glob')
    if glob_param:
        db.createGlobalParam([[glob_param,]])
    else:
        db.createGlobalParam([['NULL',]])
    if len(arr_all_file) > 0:
        i = 0
        while i < len(arr_all_file):
            # получаем исходную строку как в конфиге
            pravilo = ';'.join(arr_all_file[i])
            # Проверяем имеется ли дополнительный параметр для определения типа КЦ
            if len(arr_all_file[i]) >= 2:
                if arr_all_file[i][1] == 'f' or arr_all_file[i][1] == 'l' or arr_all_file[i][1] == 'd':
                    type_p = arr_all_file[i][1]
            else:
                type_p = 'f'
            #print(f"arr_all_file[i]== {arr_all_file[i]}")
            resul_hs_file = getFilesByCriteria(arr_all_file[i])
            #print(resul_hs_file)
            if resul_hs_file == 3:
                if type_p == 'd':
                    print("Добавление записей элемента {p} в БД ".format(p=pravilo))
                    db.createPravilo([(type_p,pravilo,i+1)])
            if resul_hs_file == 0:
                print("Не найдены объекты по данному правилу {pr}".format(pr=pravilo))
            elif resul_hs_file != 3 and resul_hs_file != 0:
                db.createFile(resul_hs_file,type_p,pravilo,i+1)
            i += 1
    else:
        #log.logM(f"Конфигурационный файл не заполнен")
        print("Конфигурационный файл не заполнен")
        quit()
# Получаем дополнительно для l хэш сумму по строчно
def checkHashSumStr(arr_element,resul_hl):
    i = 0
    #print(resul_hl)
    str_count = ''
    str_count_lang = ''
    arr_count_str = checkCountStr(resul_hl)
    
    razdn_str = arr_count_str[0][1] - arr_count_str[0][2]
    if razdn_str > 0:
        str_count = "\nСтрок добавлено: {add_s} стр".format(add_s=razdn_str)
        str_count_lang = "{txt}: {add_s} {s}".format(txt=tr("\nСтрок добавлено"),add_s=razdn_str,s=tr("стр"))
    if razdn_str < 0:
        str_count = "\nСтрок удалено: {del_s} стр".format(del_s=abs(razdn_str))
        str_count_lang = "{txt}: {del_s} {s}".format(txt=tr("\nСтрок удалено"),del_s=abs(razdn_str),s=tr("стр"))
    

    #print(f"Count - {str_count} - {arr_count_str}")
    while i < len(resul_hl):
        #print(arr_element)
        #print(resul_hl)
        j = 0
        while j < len(arr_element):
            #print(f"{arr_element[j][0]} == {resul_hl[i][0]}")
            if arr_element[j][0] == resul_hl[i][0]:
                #print(f"{arr_element[j][0]} === {resul_hl[i][0]}")
                # Когда файл поставленный на КЦ по строчно является пустым, то в БД значение строки 0
                # Следовательно отслеживать изменения будем не по строчно, а укажем целый файл что добавились строки.
                #print(arr_element[j][2] == '0')
                if arr_element[j][2] != '0':
                    #print(f"{arr_element[j][0]} == {arr_element[j][2]}")
                    if str(arr_element[j][2]) ==  str(resul_hl[i][2]):
                        #print(arr_element[j][2],resul_hl[i][2])
                        
                        if  arr_element[j][3] != resul_hl[i][1]:
                            #print(f"{arr_element[j][0]} {arr_element[j][3]} != {resul_hl[i][1]}")
                            arr_repo_str.append([arr_element[j][0],'l',arr_element[j][2],str_count,'Изменены'])
                            #print(arr_repo_str)
                            str_log = "{n_f}={file} {t_kc}={str_n} {str_n}={str_stats} {str_num} {s_w}={hs_f} {s_e}={hs_e}"\
                                .format(n_f=tr("Файл"),file=arr_element[j][0],t_kc=tr("ТипКЦ"),str_n=tr("Строка"),str_stats=arr_element[j][2],
                                    str_num=str_count_lang,s_w=tr("Было"),hs_f=arr_element[j][3],s_e=tr("Стало"),hs_e=resul_hl[i][1])
                            log.logM(str_log.replace('\n',' '))  
                            del arr_element[j]
                            break
                        else:
                            #print(arr_element[j])
                            del arr_element[j]
                            break
                else:
                    #print(f"ok {arr_element[j][0]}  ")
                    str_count = "\nСтрок добавлено: {str_add} стр".format(str_add=arr_count_str[0][1])
                    str_count_lang = "{txt}: {str_add} {s}".format(txt=tr("\nСтрок добавлено"),str_add=arr_count_str[0][1],s=tr("стр"))
                    arr_repo_str.append([arr_element[j][0],'l',arr_element[j][2],str_count,'Изменены'])
                    str_log = "{n_f}={file} {t_kc}={str_n} {str_n}={str_stats} {str_num} {s_w}={hs_f} {s_e}={hs_e}"\
                        .format(n_f=tr("Файл"),file=arr_element[j][0],t_kc=tr("ТипКЦ"),str_n=tr("Строка"),str_stats=arr_element[j][2],
                                str_num=str_count,s_w=tr("Было"),hs_f=arr_element[j][3],s_e=tr("Стало"),hs_e=resul_hl[i][1])
                    log.logM(str_log.replace('\n',' '))
                    del arr_element[j]
                    break 
            j += 1

        i += 1
# подсчет количества строк в текущем файле, и сравнение с количеством строк в БД
def checkCountStr(arr_tek):
    # Групируем массив по файлам, для поиска количества строк 
    arr_count_str = []
    for g in groupby( sorted(arr_tek,key=lambda x:x[1]) ,key=lambda x:x[0]):
        count_str = 0
        #print (f"{g[0]}")
        for i in g[1]:
            #print('-',i)
            count_str += 1
        #db.getCountStrFile(g[0],'l')
        arr_count_str.append([g[0],count_str,db.getCountStrFile(g[0],'l')[0][0]])
    #print(arr_count_str)
    return arr_count_str    
# Сравниваем общую хэш сумму файла
def checkHashSumAll(resul_h,arr_element,type_p):
     # для анализа файлов, по строчно и целиком
    i = 0
    resul_hl = []
    file_yes = ''
    #print(f"type-- {type_p}")
    #print(f" peredacha ot 1- {resul_h}")
    
    while i < len(resul_h):
        j = 0
        file_yes = ''
        if resul_h[i][2] == 'OK':
            while j < len(arr_element):

                if arr_element[j][0] == resul_h[i][0]:
                    
                    if len(resul_h[i][1]) > 1:
                        #print(arr_element[j][1].strip()!= resul_h[i][1].strip())
                        if str(arr_element[j][1]) != str(resul_h[i][1]):
                            
                            if type_p == 'l':
                                #print("ggggggg-", arr_element[j])
                                if len(file_yes) == 0: 
                                    #print(f"peredacha na hs_l - {resul_h[i][0]}")
                                    resul_hl = hashSum.hashFileReadLine([resul_h[i][0]],action_t="df")
                                    #print("res----", resul_hl)
                                    #print(f"arr----   {[arr_element[j]]}    ")
                                    file_yes = arr_element[j][0]
                                    checkHashSumStr(arr_element, resul_hl)
                                    #print(f"arr_element[j][0] {arr_element[j][0]}")
                                    
                                    break
                            else:
                                arr_repo_file.append([arr_element[j][0],type_p,'','Изменен',arr_element[j][1],resul_h[i][1]])
                                log.logM("{n_f}={file}  {t_kc}={n_f} {s_w}={hs_f} {s_e}={hs_e}"\
                                        .format(n_f=tr("Файл"),file=arr_element[j][0],t_kc=tr("ТипКЦ"),s_w=tr("Было"),
                                                hs_f=arr_element[j][1],s_e=tr("Стало"),hs_e=resul_h[i][1]))
                                break

                j += 1
        else:
            
            if type_p == 'l':
                arr_repo_str.append([resul_h[i][0],type_p,'','Файл не найден',''])
                log.logM("{f_no}={file} {t_kc}={str_n}"\
                         .format(f_no=tr("Файл не найден"),file=resul_h[i][0],t_kc=tr("ТипКЦ"),str_n=tr("Строка"))) 
            if type_p == 'f': 
                arr_repo_file.append([resul_h[i][0],type_p,'Файл не найден',''])
                log.logM("{f_no}={file} {t_kc}={n_f}"\
                         .format(f_no=tr("Файл не найден"),file=resul_h[i][0],t_kc=tr("ТипКЦ"),n_f=tr("Файл")))
     
        i += 1
  
# Анализ каталогов на предмет изменения
def checkHashSumCatal(arr_element,resul_h,type_p, pravilo=""):
    arr_elem_c = []
    arr_res_c = []
    object_not = []
    object_plus = []
    object_hs = []
    #print("catal",resul_h)
# для анализа каталогов часть
    # когда тип каталог на КЦ нужно учитывать файлы добалвенные, удаленные, изменные
    if type_p == 'd' and resul_h != 3:
 
        #print("exit")
        #start_time = time.time()
        # Распределяем общай массив по массивам из отдельных элементов, для анализа, сравнить по каталогам и по хэш сумме
        i = 0
        while i < len(arr_element):
            arr_elem_c.append(arr_element[i][0])
            i += 1
        i = 0
        while i < len(resul_h):
            arr_res_c.append(resul_h[i][0])
            i += 1
        #print("--- %s итер1 ---" % (time.time() - start_time))
        #start_time = time.time()
        #[x for t in Ans for x in t]
        # находим разность между что было и что сейчас имеется
        result = list(set(arr_elem_c) - set(arr_res_c))
        # находим пересечение и получаем отсутствующие файлы в объектах поставленых на КЦ
        object_not.append(list(set(arr_elem_c) & set(result)))
        # находим файлы которые были добавлены
        result.clear()
        # находим разность между что щас и что было, получаем новые файлы
        result = list(set(arr_res_c) - set(arr_elem_c))
        #print("--- %s итер2 ---" % (time.time() - start_time))
        #start_time = time.time()
        #print("RES",arr_res_c)
        #print("ELEM",arr_elem_c)
        object_plus.append(result)
        #print("ADD",object_plus)
        o_p = 0
        while o_p < len(object_plus[0]):
            #print(f"Chast - {object_plus[0][o_p].rpartition('/')[0]}")
            arr_repo_catal.append([object_plus[0][o_p].rpartition('/')[0],type_p,"fa:{fa}"
                                   .format(fa=object_plus[0][o_p].rpartition('/')[2]),''])
            #mytable.add_row([object_plus[0][o_p],type_p,'yes','-','-'])
            o_p += 1
        #result=list(set([x for t in arr_element for x in t]) & set([x for t in resul_h for x in t]))
        # находим пересечение тем самым определяем какие файлы удалились
        result.clear()
        result = list(set(arr_elem_c) & set(arr_res_c))
        o_n = 0
        while o_n < len(object_not[0]):
            arr_repo_catal.append([object_not[0][o_n].rpartition('/')[0],type_p,"fu:{fu}"
                                   .format(fu=object_not[0][o_n].rpartition('/')[2]),''])
            #mytable.add_row([object_not[0][o_n],type_p,'-','del','-'])
            o_n += 1
        #print("--- %s итер3 ---" % (time.time() - start_time))
        #start_time = time.time()

        i = 0
        db.createAnalosis(resul_h)
        err_file = db.getFileError(pravilo)
        #print(err_file)
        #quit()
        
        while i < len(err_file):
            #print(err_file[i][0].rpartition('/')[0],type_p,'',"hs:{hs}".format(hs=err_file[i][0].rpartition('/')[2]))
            arr_repo_catal.append([err_file[i][0].rpartition('/')[0],type_p,'',"hs:{hs}".format(hs=err_file[i][0].rpartition('/')[2])])
            i += 1
        
        db.deleteTableAllData('analisis')
        #print("--- %s итер4 ---" % (time.time() - start_time))
# Анализ элементов
def analysisElem(arr_object_db,arr_arr_element):
    #print("obj",arr_object_db)
    j = 0
    #print(arr_arr_element)
    while j < len(arr_object_db):
        resul_h = []
        #print("id_element",arr_object_db[j])
        # получаем информацию по элементу в виде объектов
        #arr_element = db.getElementData(arr_object_db[j][1])
        arr_element = arr_arr_element[j]
        arr_vr = []
        # Получаем хэш сумму объектов
        if arr_object_db[j][0] == 'd':
            
            resul_h = getFilesByCriteria(arr_object_db[j][2].split(';'))
            #print("d---",resul_h)
            if resul_h != 0:
                checkHashSumCatal(arr_element,resul_h,arr_object_db[j][0],pravilo=arr_object_db[j][2])
            else:
                print("\nОбъект по данному правилу {o} не найден".format(o=arr_object_db[j][2]))
        else:     
            i = 0   
            while i < len(arr_element):
                arr_vr.append(arr_element[i][0])
                i += 1
            if arr_object_db[j][0] == 'l':
                get_items_f = list(set(arr_vr))
                #print(get_items_f)
                #resul_h = hashSum.hashFileReadLine(list(set(arr_vr)))
                resul_h = hashSum.hashFileAll(get_items_f,time_lim=time_limit,max_threading=max_threading)
                #print(f"1operation - {resul_h}")
                checkHashSumAll(resul_h,arr_element,arr_object_db[j][0])
                
                #print(list(set([x for t in resul_h for x in t])))         
            if arr_object_db[j][0] == 'f':
                resul_h = hashSum.hashFileAll(arr_vr,time_lim=time_limit,max_threading=max_threading)
                #print(resul_h)
                checkHashSumAll(resul_h,arr_element,arr_object_db[j][0])
        j += 1    
          
# Функция нахождения последовательности в списке элементов.
def getSequences(seq):
    #print(f"seq-  {seq}")
        res = []
        sub_seq = seq[0]
        first_n = sub_seq
        last_n = 0
        i = 1
    #if len(seq) >= 1:
        while i < len(seq):
            if (seq[i] - sub_seq) == 1:
                if i == len(seq)-1:
                    #print(f"1 {first_n}  - {seq[i]}")
                    if first_n - seq[i] == 0:
                        res.append([first_n])
                    else:
                        res.append([first_n,seq[i]])
                sub_seq = seq[i]
                
            else:
                last_n = seq[i-1]
                #print(f"2 {first_n}  -  {last_n}")
                if first_n - last_n == 0:
                    res.append([first_n])
                else:
                    res.append([first_n,last_n])
                sub_seq = seq[i]
                first_n = sub_seq
                if i == len(seq)-1:
                    #print(f"3 {first_n}  - {seq[i]}")
                    if first_n - seq[i] == 0:
                        res.append([first_n])
                    else:
                        res.append([first_n,seq[i]])
            i += 1
        #else:
        #    res.append([seq[0]])
        return res  
# Формируем итоговый отчет по КЦ файлов по строчно.      
def otchetFileStr():
    #otchet_f_str = []
    res_arr_group = []
    #print(arr_repo_str)
    # Групируем массив по файлам, затем в каждой группе что бы не дублировать имя файла оставляем первую строку пустую
    for g in groupby( sorted(arr_repo_str,key=lambda x:x[0]) ,key=lambda x:x[0]):
        #print (f"{g[0]}")
        arr_number_str = []
        
        for i in g[1]:
            #print(i)
            if i[2]:
                arr_number_str.append(int(i[2]))
        if i[2]:
            #print(f"arr_n-- {len(arr_number_str)}")
            if len(arr_number_str) > 1:
                res_arr_group = getSequences(arr_number_str)
            else:
                res_arr_group = [arr_number_str]

            j = 0
            str_number = ''
            while j < len(res_arr_group):
                if len(res_arr_group[j]) > 1:
                    str_number += "{s1}-{s2};".format(s1=res_arr_group[j][0],s2=res_arr_group[j][1])
                else:
                    str_number += "{s1};".format(s1=res_arr_group[j][0])
                j += 1
            arr_number_str.clear()
            #print(f"{str_number} -- {i}")
            otchet_f_str.append([g[0],str_number[:-1],"{p1}{p2}".format(p1=i[4],p2=i[3])])
        else:
            otchet_f_str.append([g[0],'',"{p1}{p2}".format(p1=i[4],p2=i[3])])
    ii = 0
    while ii <len(otchet_f_str):
        mytable_str.add_row(otchet_f_str[ii])
        #print(test_a[ii])
        ii += 1   
    #print(mytable_str)
    #print(arr_repo_str)
#Формируем итоговый отчет для файлов. что бы сохранить нужную информацию в массиве, реализуем выборку отдельной функцией.      
def otchetFile():
    i = 0
    while i < len(arr_repo_file):
        mytable_file.add_row([arr_repo_file[i][0],"{s1}{s2}"
            .format(s1=arr_repo_file[i][2],s2=arr_repo_file[i][3])])
        i += 1
    #print(mytable_file)
#Формируем итоговый отчет по каталогам
def otchetCatalog():
    # Групируем массив по каталогам
    #print(arr_repo_catal[0])
    for g in groupby( sorted(arr_repo_catal,key=lambda x:x[0]) ,key=lambda x:x[0]):
        #print (f"{g[0]}")
        str_otchet_remove = 'Не найдены файлы:\n'
        str_otchet_add = 'Добавлены файлы:\n'
        str_otchet_chang = 'Изменены файлы:\n'
        str_otchet_remove_lang = '{f_no}:\n'.format(f_no=tr("Не найдены файлы"))
        str_otchet_add_lang = '{f_a}:\n'.format(f_a=tr("Добавлены файлы"))
        str_otchet_chang_lang = '{f_c}:\n'.format(f_c=tr("Изменены файлы"))
        rem = 0
        add_f = 0
        chang = 0
        str_count = 0
        for i in g[1]:
            remove_add = i[2]
            changed = i[3]
            #print("-",i)
            if str_count < 4:
                if remove_add[0:3] == 'fu:':
                    str_otchet_remove += "{str_a}; ".format(str_a=remove_add[3:])
                    str_otchet_remove_lang += "{str_a}; ".format(str_a=remove_add[3:])
                if remove_add[0:3] == 'fa:':
                    str_otchet_add += "{str_a}; ".format(str_a=remove_add[3:])
                    str_otchet_add_lang += "{str_a}; ".format(str_a=remove_add[3:])
                if changed[0:3] == 'hs:':
                    str_otchet_chang += "{str_c}; ".format(str_c=changed[3:])
                    str_otchet_chang_lang += "{str_c}; ".format(str_c=changed[3:])
                str_count += 1
            else:
                if remove_add[0:3] == 'fu:':
                    str_otchet_remove += "\n{str_a}; ".format(str_a=remove_add[3:])
                    str_otchet_remove_lang += "\n{str_a}; ".format(str_a=remove_add[3:])
                if remove_add[0:3] == 'fa:':
                    str_otchet_add += "\n{str_a}; ".format(str_a=remove_add[3:])
                    str_otchet_add_lang += "\n{str_a}; ".format(str_a=remove_add[3:])
                if changed[0:3] == 'hs:':
                    str_otchet_chang += "\n{str_c}; ".format(str_c=changed[3:])
                    str_otchet_chang_lang += "\n{str_c}; ".format(str_c=changed[3:])
                str_count = 0
            
        if len(str_otchet_chang) == len('Изменены файлы:\n'):
            str_otchet_chang = ''
            str_otchet_chang_lang = ''
            chang = 1
        else:
            str_otchet_chang = str_otchet_chang[:-2]
            str_otchet_chang_lang = str_otchet_chang_lang[:-2]
        if len(str_otchet_remove) == len('Не найдены файлы:\n'):
            str_otchet_remove = ''
            str_otchet_remove_lang = ''
            rem = 1
        else:
            str_otchet_remove = str_otchet_remove[:-2]
            str_otchet_remove_lang = str_otchet_remove_lang[:-2]
        if len(str_otchet_add) == len('Добавлены файлы:\n'):
            str_otchet_add = ''
            str_otchet_add_lang = ''
            add_f = 1
        else:
            str_otchet_add = str_otchet_add[:-2]
            str_otchet_add_lang = str_otchet_add_lang[:-2]

        if rem == 0 and add_f == 0 and chang == 0:
            str_otchet_remove += "\n"
            str_otchet_remove_lang += "\n"
            str_otchet_add += "\n"
            str_otchet_add_lang += "\n"
        else:
            if (rem == 0 and chang == 0) or (rem == 0 and add_f == 0) :
                str_otchet_remove += "\n"
                str_otchet_remove_lang += "\n"
            if add_f == 0 and chang == 0:
                str_otchet_add += "\n"
                str_otchet_add_lang += "\n"      
        #print(f"{str_otchet_remove}{str_otchet_add}{str_otchet_chang}")
        str_log = "{c_n}={file} {file_d}{file_a}{file_c}"\
            .format(c_n=tr("Каталог"),file=g[0],file_d=str_otchet_remove_lang,file_a=str_otchet_add_lang,file_c=str_otchet_chang_lang)
        log.logM(str_log.replace('\n',' '))
        otchet_d_cat.append([g[0],"{file_d}{file_a}{file_c}"
            .format(file_d=str_otchet_remove,file_a=str_otchet_add,file_c=str_otchet_chang)])
        mytable_catalog.add_row([g[0],"{file_d}{file_a}{file_c}"
            .format(file_d=str_otchet_remove,file_a=str_otchet_add,file_c=str_otchet_chang)])
    #print(mytable_catalog)
#Печать отчета в консоль в упрощенном варианте
def consolOtchet():
    if len(otchet_f_str) > 0:
        print("Тип проверки - изменение файлов построчно (Тип КЦ \"l\")")
        i = 0
        while i < len(otchet_f_str):

            #print(' '.join(otchet_f_str[i]))
            str_l_f = "Файл: {file}. № Строки: {str_n}. Состояние: {str_stats}"\
                .format(file=otchet_f_str[i][0],str_n=otchet_f_str[i][1],str_stats=otchet_f_str[i][2])
            print(str_l_f.replace('\n','. '))  
            i += 1
    if len(otchet_d_cat) > 0:
        print("Тип проверки - изменение каталогов (Тип КЦ \"d\")")
        i = 0
        while i < len(otchet_d_cat):
            str_d_f = otchet_d_cat[i][1]
            str_d_f = str_d_f.replace('\n',' ')
            str_d_f = str_d_f.replace(' Добавлены файлы','. Добавлены файлы')
            str_d_f = str_d_f.replace(' Изменены файлы','. Изменены файлы')
            str_d_f = str_d_f.replace(' Не найдены файлы','. Не найдены файлы')
            print("Каталог: {catal}. Состояние: {str_stats}".format(catal=otchet_d_cat[i][0],str_stats=str_d_f))
            i += 1
    if len(arr_repo_file) > 0:
        print("Тип проверки - изменение файлов (Тип КЦ \"f\")")
        i = 0
        while i < len(arr_repo_file):
            print("Файл: {file}. Состояние: {str_stats}{str_c}".format(
                file=arr_repo_file[i][0],str_stats=arr_repo_file[i][3],str_c=arr_repo_file[i][2]
            ))
            i += 1
    if len(otchet_d_cat) < 1 and len(arr_repo_file) < 1 and len(otchet_f_str) < 1:
        print("Проверка КЦ завершилась. Различий в объектах не выявлено")
# Печать табличного отчета в консоль
def tableOtchet():
    if len(otchet_f_str) > 0:
        print("Тип проверки - изменение файлов построчно (Тип КЦ \"l\")")
        mytable_str.align = "l"
        mytable_str._max_width = {"Файл":60,"№ Строки":100}
        print(mytable_str)   
    if len(arr_repo_file) > 0:
        print("Тип проверки - изменение файлов (Тип КЦ \"f\")")
        mytable_file.align = "l"
        mytable_file._max_width = {"Файл":60}
        print(mytable_file)
    if len(otchet_d_cat) > 0:    
        print("Тип проверки - изменение каталогов (Тип КЦ \"d\")")
        mytable_catalog.align = "l"
        mytable_catalog._max_width = {"Каталог":60,"Состояние":100}
        print(mytable_catalog)
    if len(otchet_d_cat) < 1 and len(arr_repo_file) < 1 and len(otchet_f_str) < 1:
        print("Проверка КЦ завершилась. Различий в объектах не выявлено")
# Функция получения элементов, и распределение по потокам
def trackedItems(number_obj="",type_otchet="",time_lim=""):
    global time_limit
    time_limit = time_lim
    arr_elem = []
    #start_time = time.time()
    if number_obj:
        arr_elem = db.getElement(number_obj)
    else:
        # Получаем массив элементов, дальше вынести в отдельный поток данную операцию
        arr_elem = db.getElementAll()
    #print(arr_elem)
       
    # проверка что не пустой массив вернулся
    if len(arr_elem) > 0:
        
        if len(arr_elem) != max_threading:
                # перебираем все элементы, и дальше каждый элемент в новый   поток
                i = 0
                while i < len(arr_elem):                  
                    arr_element = db.getElementData(arr_elem[i][1]) 
                    analysisElem([arr_elem[i]],[arr_element])                    
                    i += 1

        otchetFileStr()
        otchetFile()
        otchetCatalog()
        #print("--- %s seconds1 ---" % (time.time() - start_time))
        if type_otchet == 'console':
            consolOtchet()
        else:
            tableOtchet()
    else:
        log.logM(tr("В БД не найдены объекты для проверки КЦ"))
#trackedItems()
#checkKC()
