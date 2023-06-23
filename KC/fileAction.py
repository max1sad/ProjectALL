import os
import glob
import loggerS as log
import re
from pathlib import Path 
from allFunction import read_file
from dbProvide import getGlobalParam

# Получение списка файлов если в конфиге указан 1 параметр через разделитель, считаем что указано файл или каталоги, включая регулярные выражения
def fileDir(file):
    files = glob.glob(file)
    return files
#print(fileDir('/tmp/test/**/*'))

def checkExeptCatal(all_catal):
    # Системные исключения файловой системы и примонтированные устройства
    exec_system =  read_file('/proc/filesystems')
    mount_dev = os.popen("mount").readlines()
    #print(mount_dev[0].split(" ")[2])
    # выявляем все устройства которые попадают под исключения
    iskl_arr = []
    mount_all_arr = []
    resul = []

    i = 0
    check_all = 0
    while i < len(exec_system):
        str_vr = exec_system[i].strip()
        str_exec_ar = str_vr.split("\t")
        
        if str_exec_ar[0] == 'nodev':
            for str_dev in mount_dev:
                
                str_dev_vr = str_dev.strip()
                str_dev_ar = str_dev_vr.split(" ")
                if check_all == 0:
                    mount_all_arr.append(str_dev_ar[2])
                if str_exec_ar[1] == str_dev_ar[4]:
                    # получили список примонтирвоанных устройств, попадающих в исключение
                    iskl_arr.append(str_dev_ar[2])
        check_all = 1
        i += 1
    # Список разрешенных примонтированных устройств.
    yes_mount = list(set(mount_all_arr) ^ set(iskl_arr))
    # На вход каталоги поступат, котрые были ракрыты через регулярку, или без раскрытия существуют уже
    i = 0
    n = len(all_catal)
    while i < n:
        # обход по запрещенным устройствам
        j = 0
        catal_check = all_catal[i]
        if catal_check[len(catal_check)-1] != "/":
            catal_check += "/"
        while j < len(iskl_arr):
                #print(catal_check)
            match = re.search("^"+iskl_arr[j]+"/",catal_check)
            if match:
                    jj = 0
                    check_catal = 0
                    while jj < len(yes_mount):
                        if yes_mount[jj] != "/":
                            match_jj = re.search(yes_mount[jj],catal_check)
                            if match_jj:
                                check_catal = 1
                        jj += 1
                    if check_catal == 0:
                        resul.append(all_catal[i])
                        #print(f"{iskl_arr[j]}   {catal_check}")
                    #n -= 1
            j += 1
        i += 1
    if len(resul) > 0:
        print("Объекты не подлежат постановке на КЦ:",";".join(resul))
    #print(all_catal)
    return list(set(resul) ^ set(all_catal))
    #print(yes_mount)


def catalogAndRex(str_all):
    arr_param = str_all.split('/')
    i = 0
    str_path = ''
    path_yes = ''
    path_re = ''
    while i < len(arr_param):
        str_path += arr_param[i] + "/"
        if os.path.isdir(str_path) or os.path.isfile(str_path):
            path_yes += arr_param[i] + "/"
        else:
            path_re += arr_param[i] + "/"
        i += 1
    #print(fileAction.glob_re([path_yes,path_re[:len(path_re)-1]],regex=".*"))
    return [path_yes,path_re[:len(path_re)-1]]
# glob_mask="**/*" - по всем деректориям поиск
# glob_mask="*" - только по текущей
def glob_re(path,regex="", glob_mask="*", inverse=False, count_obj_yes="",global_conf=""):
        #print(f"path  {path}  reg  {regex}")
        i = 0
        resul = []
        file_all = []
        sum_obj = 0
        res = []
        path = checkExeptCatal(path)
        #print("path:",path)
        #count_obj_yes = readFileConf('SETTING','count_object')
        if len(global_conf) > 2:
            global_vr_db = global_conf
        else:
            global_vr_db = getGlobalParam()[0][0]
        #global_vr_db = getGlobalParam()[0][0]
        #print("global",global_vr_db)
        if len(global_vr_db) > 0:
            if global_vr_db == 'NULL':
                global_regex = ''
            else:
                global_regex = global_vr_db
        #print(global_regex)
        while i < len(path):
            #file_all.clear()
            p = Path(path[i])
            if regex:
                regex_all = "{p1}/{p2}".format(p1=p,p2=regex)
                #print(regex_all)
            else:
                regex_all=''
            if inverse:
                res = [str(f) for f in p.glob(glob_mask) if not re.search(regex_all, str(f))]
            else:
                try:
                    res = [str(f) for f in p.glob(glob_mask)  if re.search(regex_all, str(f))] 
                except Exception as e:
                    print("\nВ каталоге {cat} содержатся файлы содержащие слишком много уровней символьных ссылок".format(cat=p))
            #print(res)
            if len(res) > 0:
                #if glob_mask == '**/*':
                    j = 0
                    while j < len(res):
                        if os.access(res[j],os.R_OK):
                            if os.path.isfile(res[j]):
                                if global_regex:
                                    match = re.search(global_regex,res[j].rpartition('/')[2])
                                    if not match:
                                        file_all.append(res[j])
                                else:
                                    file_all.append(res[j])
                        else:
                             print("\nОтказано в доступе {file}".format(file=res[j]))
                        sum_obj += 1       
                        j += 1
                    #print(file_all)
                    #resul.concatenate([resul, file_all])
                    #resul.append(file_all)
            #print(resul)
                #else:
                #   resul.append(res) 
            i += 1  
        resul.append(file_all)  
        if sum_obj > int(count_obj_yes):
            print("\nПревышено максимальное количество объектов для анализа!")   
        #print(resul)
        return resul
#res = glob_re(['/usr/'],glob_mask="**/*",count_obj_yes=5)
#print(res)
# Проверка глобального ограничения для существующего файла, без раскрытия регулярки.
def checkFileRegGlobal(file,global_conf=""):
    file1 = checkExeptCatal([file])
    #print("file",file)
    arr_obj = []
    if len(file1) > 0:
        file = file1[0]
        if len(global_conf) > 2:
            global_vr_db = global_conf
        else:
            global_vr_db = getGlobalParam()[0][0]
        #global_vr_db = getGlobalParam()[0][0]
        if len(global_vr_db) > 0:
                if global_vr_db == 'NULL':
                    global_regex = ''
                else:
                    global_regex = global_vr_db
        
        if global_regex:
            match = re.search(global_regex,file)
                                    
            if not match:
                arr_obj.append(file)
        else:
            arr_obj.append(file)
    return arr_obj

def allDir(dir,type_c="d",global_conf=""):
    arr_obj = []
    i = 0
    if type_c != "d":
        dir = checkExeptCatal(dir)
    if len(global_conf) > 2:
        global_vr_db = global_conf
    else:
        global_vr_db = getGlobalParam()[0][0]
    if len(global_vr_db) > 0:
            if global_vr_db == 'NULL':
                global_regex = ''
            else:
                global_regex = global_vr_db
    while i < len(dir):
        if os.access(dir[i],os.R_OK):
            for catalog in os.listdir(dir[i]):
                if type_c == 'd':
                    if os.path.isdir(os.path.join(dir[i],catalog)):
                        arr_obj.append(os.path.join(dir[i],catalog))
                if type_c == 'f':
                    if os.path.isfile(os.path.join(dir[i],catalog)):
                        if global_regex:
                            match = re.search(global_regex,catalog)
                                    
                            if not match:
                                arr_obj.append(os.path.join(dir[i],catalog))
                        else:
                            arr_obj.append(os.path.join(dir[i],catalog))
        else:
             print("\nОтказано в доступе {file}".format(file=dir[i]))
        i += 1
    
    return arr_obj
#print(allDir(['/tmp/test/'],'f'))
def regexObj(path_all,type_c,global_conf=""):
    #path_all = '/tmp/test/[13]/[0-9]/'
    i = 0
    j = 0
    cou = 1
    arr_catal = []
    #print(path_all, "ggg")
    # Получаем массив где левая часть путь до каталога без регулярки, правая сама регулярка
    arr_c_r = catalogAndRex(path_all)
    #print(arr_c_r)
    # разделяем регулярку на массив
    str_reg = arr_c_r[1]
    if str_reg[len(str_reg)-1] == '/':
        cou = 0
        str_reg = str_reg[:len(str_reg)-1]
    if type_c == 'd':
        cou = 0
    arr_regex = str_reg.split('/')
    arr_catal.append(arr_c_r[0])
    # Цикл по количеству регулярных выражений, сколько раз нужно раскрывать регулярку
    while i < len(arr_regex)- cou:
        # Передаем каталоги без регулярки и получаем список текущих каталогов
        arr_dir = allDir(arr_catal,global_conf=global_conf)
        
        arr_catal.clear()
        # запускаем цикл по обходу элементов с раскрытием регулярного выражения
        while True:
            if len(arr_dir) > 0 and j < len(arr_dir):
                # проверка регулярного выражения
                #print(arr_regex[i],arr_dir[j].rpartition('/')[2])
                try:
                    match = re.search("^"+arr_regex[i]+"$",arr_dir[j].rpartition('/')[2])
                except:
                    print("Ошибка раскрытия правила",path_all)
                    quit()
                if match:
                    #print(arr_dir[j],arr_dir[j].rpartition('/')[2])
                    arr_catal.append(arr_dir[j])
            else:
                break
            j += 1  
        j = 0
        i += 1
    #print("arr_catal",arr_catal)
    return checkExeptCatal(arr_catal)
