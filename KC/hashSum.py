import hashlib as hs
import parcerStr
import loggerS as log
import os
#import sys
import subprocess as subp
#from progress.bar import Bar
from math import ceil
from threading import Thread
import threading
import time
#import itertools
from waitProcess import startEx, stopEx
from translator import tr
resul_all =[]

# Хэш сумма с файла целиком. на вход принимает массив файлов
def hashFileAll(file_arr,time_lim="",max_threading=""):
        #print("Получение хэш суммы файлов")
        #startEx()
        #print(len(file_arr))
        #start_time = time.time()
        threads = []
        len_obj = len(file_arr)
        #max_threading = 10
        resul_all.clear()
        #bar = Bar('Processing', max=max_threading)
        if len_obj > max_threading:
            k_e = 0
            vr_n = 0
            max_thr = max_threading    
            for n in range(max_thr):
                if ceil(len_obj/max_thr) == len_obj/max_thr:
                    k_e = len_obj/max_thr
                else:
                    k_e = ceil(len_obj/max_thr)
                    len_obj = len_obj - ceil(len_obj/max_thr)
                    max_thr = max_thr - 1
                #print(file_arr[vr_n:int(k_e) + vr_n])
                vr_arr = file_arr[vr_n:int(k_e) + vr_n]
                #print("vr",vr_arr)
                t = Thread(target=dublHsThreads,args=(vr_arr,time_lim))
                threads.append(t)
                t.start()
                vr_n = int(k_e) + vr_n
                
        if len(file_arr) <= max_threading:
            i = 0
            #print("gg333")
            while i < len(file_arr):
                    #print(file_arr[i])
                    t = Thread(target=dublHsThreads,args=([file_arr[i]],time_lim))
                    threads.append(t)
                    t.start()
                    
                    i += 1
        #print("Count",threading.active_count())
        # ждем, когда потоки выполнятся
        for t in threads:
            t.join()
        #stopEx()
        #print("--- %s seconds ---" % (time.time() - start_time))
        return resul_all

def md5s(filen):
    md5_hash = hs.md5()
    with open(filen,"rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            md5_hash.update(byte_block)
        return md5_hash.hexdigest()
    
def dublHsThreads(file_arr,time_lim=""):
        i = 0
        err_ar_all = []
        #print(file_arr)
        #bar = Bar('Processing', max=len(file_arr))
        while i < len(file_arr):
            #print(file_arr[i])
            res = ''
            if parcerStr.checkFileOrCatalog(file_arr[i]) == 2:
                
                try:
                        if os.access(file_arr[i], os.R_OK):
                            #print(file_arr[i])
                            if len(time_lim) > 0:
                                start_time=time.time()
                                
                                #while (time.time() - start_time) < time_lim:
                                #    print("fff")
                                res = md5s(file_arr[i])
                                    #break
                                    #  pass # ваши действия
                                #print(res)
                                #res = subp.run(['timeout',str(time_lim)+"s",'md5sum','{file}'.format(file=file_arr[i])],stdout=subp.PIPE, stderr=subp.PIPE)
                                
                            else:
                                #res = subp.run(['md5sum','{file}'.format(file=file_arr[i])],stdout=subp.PIPE, stderr=subp.PIPE)
                                res = md5s(file_arr[i])
                            #print("gg")
                            #if len(res.stderr) > 1:
                            if len(res) < 1:
                                print("Ошибка снятия хэш суммы с файла: {f}".format(f=file_arr[i]))
                            else:
                                #if len(time_lim) > 0:
                                #    md5_returned = res.stdout
                                #    md5_returned = str(md5_returned)[2:].split(" ")[0]
                                #else:
                                md5_returned = res
                                if len(md5_returned) > 5:
                                    #print(str(md5_returned)[2:].split(" ")[0])
                                    #md5_returned = os.popen("md5sum {file}".format(file=file_arr[i]))
                                    # Добавляем в массив результат
                                    #resul.append([file_arr[i],md5_returned.read().split(' ')[0],'OK'])
                                    #resul_all.append([file_arr[i],str(md5_returned)[2:].split(" ")[0],'OK'])
                                    resul_all.append([file_arr[i],md5_returned,'OK'])
                                else:
                                    err_ar_all.append("Файл большого объема, превышен лимит ожидания {file}".format(file=file_arr[i]))
                                    #print("Файл большого объема превысил лимит ожидания {file}".format(file=file_arr[i]))
                        else:
                            #print("Отказано в доступе {file}".format(file=file_arr[i]))
                            err_ar_all.append("Отказано в доступе {file}".format(file=file_arr[i]))
                            #resul.append([file_arr[i],'-','NO'])
                        
                        #print(resul)
                except Exception as e:
                    #resul.append([file_arr[i],'-','NO'])
                    #print("Неудалось прочитать файл {file}".format(file=file_arr[i]))
                    log.logM("{txt} {file}".format(txt=tr("Не удалось прочитать файл"),file=file_arr[i]))
                    resul_all.append([file_arr[i],'-','NO'])
                    #break
            else:
                #pass
                resul_all.append([file_arr[i],'-','NO'])
            #bar.next()
            i += 1
    #print(resul)
        #bar.finish()
        if len(err_ar_all) > 0:
            print("\n".join(err_ar_all))
        #print(resul_all)
        #return resul_all

# Получение Хэш суммы полного файла
def hashFile(file_p,time_lim=""):
    err_ar = []
    resul = ''
    #print("time_l",time_lim)
    if os.access(file_p, os.R_OK):
        #print(file_p)
        if len(time_lim) > 0:
            #start_time=time.time()
            #while (time.time() - start_time) < time_lim:

            res = md5s(file_p)
            #    break
            #print(str(time_lim)+"s")
            #res = subp.run(['timeout',str(time_lim)+"s",'md5sum','{file}'.format(file=file_p)],stdout=subp.PIPE, stderr=subp.PIPE)                   
        else:
            res = md5s(file_p)
            #res = subp.run(['md5sum','{file}'.format(file=file_p)],stdout=subp.PIPE, stderr=subp.PIPE)
                        #print("gg")
        if len(res) < 1:
            print("Ошибка снятия хэш суммы с файла: {f}".format(f=file_p))
        else:
            #if len(time_lim) > 0:
            #    md5_returned = res.stdout
            #    md5_returned = str(md5_returned)[2:].split(" ")[0]
            #else:
            md5_returned = res
            if len(md5_returned) > 5:
                                #print(str(md5_returned)[2:].split(" ")[0])
                                #md5_returned = os.popen("md5sum {file}".format(file=file_arr[i]))
                                # Добавляем в массив результат
                                #resul.append([file_arr[i],md5_returned.read().split(' ')[0],'OK'])
                resul = md5_returned
            else:
                err_ar.append("Файл большого объема, превышен лимит ожидания {file}".format(file=file_p))
                                #print("Файл большого объема, превышен лимит ожидания {file}".format(file=file_arr[i]))
    else:
                        #print("Отказано в доступе {file}".format(file=file_arr[i]))
        err_ar.append("Отказано в доступе {file}".format(file=file_p))
    
    return resul, err_ar
# Получаем хэш сумму  одного файла на вход принимает массив файлов
def hashFileReadLine(file_arr,action_t='',time_lim=""):
    err_ar = []
    resul =[]
    i = 0
    j = 0
    hsSum = ''
    check_er = 0
    #print("file_arr-",file_arr)
    #print("ar",action_t)
    err_t = []
    while i < len(file_arr):
        if len(action_t) > 2:
            hsSum,err_t = hashFile(file_arr[i],time_lim=time_lim)
            #print("hsss",hsSum)
        if parcerStr.checkFileOrCatalog(file_arr[i]) == 2:
            #print(file_arr[i])
            try:
                with open(str(file_arr[i]),'r') as file_to_check:
                    
                    try:
                        # читаем содержимое файла  
                        data = file_to_check.readlines()
                    except Exception as ee:
                        log.logM("{txt} {file}".format(txt=tr("Файл не подлежит для построчного анализа"),file=file_arr[i]))
                        err_ar.append("Файл {file} не подлежит для построчного анализа".format(file=file_arr[i]))
                        check_er = 1
                        #break
                    if check_er == 0:
                        md5_returned_all = hsSum
                        if len(data) == 0:
                            #data = file_to_check.read()
                            #md5_returned = hs.md5(data.encode('UTF-8')).hexdigest()
                            
                            if len(action_t) > 2:
                                # Добавляем в массив результат
                                resul.append([file_arr[i],md5_returned_all,0,md5_returned_all])
                            else:
                                #print("suda")
                                # получаем хэш сумму файла
                                #md5_returned = hs.md5(data.encode('UTF-8')).hexdigest()
                                # Добавляем в массив результат
                                resul.append([file_arr[i],md5_returned_all,0,'OK'])
                        else:
                            #if len(action_t) > 2:
                                #data1 = file_to_check.read()
                                #md5_returned1 = hs.md5(data1.encode('UTF-8')).hexdigest()
                                #print(md5_returned1)
                            co = 1
                            for str_f in data:
                                # получаем хэш сумму файла
                                md5_returned = hs.md5(str_f.encode('UTF-8')).hexdigest()
                                # Добавляем в массив результат
                                if len(action_t) > 2:
                                    #print(md5_returned,md5_returned_all) 
                                    resul.append([file_arr[i],md5_returned,co,md5_returned_all])
                                else:
                                    resul.append([file_arr[i],md5_returned,co,'OK'])
                                co += 1
                    else:
                        check_er = 0
                        
            except Exception as e:
                if check_er == 0:
                #print("Не удалось прочитать файл {file}".format(file=file_arr[i]))
                    log.logM("{txt} {file}".format(txt=tr("Не удалось прочитать файл"),file=file_arr[i]))
                    err_ar.append("Не удалось прочитать файл {file}".format(file=file_arr[i]))
                else:
                    check_er = 0
                #resul.append([file_arr[i],'-','-','NO'])
                #break
        else:
            resul.append([file_arr[i],'-','-','NO'])
       
       
        i += 1
    #print(resul)
    if len(err_ar) > 0:
        print("\n".join(err_ar))
    if len(err_t) > 0:
        print("\n".join(err_t))
    
    return resul

                
#print(hashSumOneFile('/tmp/test/t1/y.conf'))
# Хэш сумма строчки в файле, на вход путь и номер строки
#def hashSumOneStr(path,num_str):
    
#print(hashFileReadLine(['/tmp/test/1.txt'],action_t="r"))
