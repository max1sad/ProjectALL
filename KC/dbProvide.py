from dbConnect import getSqldata,createData,delteData,connectDb,createCursor
import time
connect = ''
cursor = ''
def connectDataBase(path_db):
    
    global connect
    global cursor
    
    connect = connectDb(path_db)
    cursor = createCursor(connect)
# Запросы на получение данных
def getFileAll():
    sqlite_select_query = "select * from fileInf;"
    result = getSqldata(sqlite_select_query,cursor)
    return result
def getFileAllPravilo(id_p):
    sqlite_select_query = "select id_file,name_file from fileInf where id_p = {p};".format(p=id_p)
    result = getSqldata(sqlite_select_query,cursor)
    return result
def getIdFile(id_file,id_p):
    #print(id_p)
    sqlite_select_query = "select id_file from fileInf where name_file = '" + str(id_file) + "' and id_p = {p};".format(p=id_p)
    result = getSqldata(sqlite_select_query,cursor)
    return result
def getCoutnFileInf():
    sqlite_select_query = "select COUNT(*) as c from fileInf;"
    result = getSqldata(sqlite_select_query,cursor)
    return result
def getParameters(prav):
    sqlite_select_query = "select id_p as c from parameters where parav = '" + str(prav) + "';"
    result = getSqldata(sqlite_select_query,cursor)
    return result
# Получаем указанное правило для поставноки объектов на КЦ, по номеру правила
def getParametersNum(number_prav):
    sqlite_select_query = "select parav,type_p,id_p from parameters where number = '" + str(number_prav) + "';"
    result = getSqldata(sqlite_select_query,cursor)
    return result
#print(getParametersNum('1'))
#print(getFileAll())
#print(getCoutnFileInf()[0][0] == 6)
# получаем все данные из БД для дальнейшего анализа
def getElementData(id_p):
    
    sqlite_select_query =(
        "select name_file, sum_file_all,num_str,sum_file_str from fileInf "\
            "inner join md5sum_file  on fileInf.id_file = md5sum_file.id_file "\
            "where fileInf.id_p = '{id_p}' ".format(id_p=id_p)
    )
    
    result = getSqldata(sqlite_select_query,cursor)
    return result

# получаем количество записей в БД по конкретному файлу
def getCountStrFile(name_file,type_p):
    sqlite_select_query =(
        "select COUNT(*) from fileInf inner join md5sum_file "\
            "on fileInf.id_file = md5sum_file.id_file join parameters "\
            "on fileInf.id_p = parameters.id_p "\
            "where parameters.type_p == '{ty}' and fileInf.name_file = '{file}' "\
            "group by fileInf.name_file".format(ty=type_p,file=name_file)
    )
    result = getSqldata(sqlite_select_query,cursor)
    return result
#print(getCountStrFile('/tmp/test/t2/g.conf','l')[0][0])
#print(getElementData('108'))
# проверка на дублирующиеся файлы с БД по типу правила
def getFileDublicate():
    sqlite_select_query =(
    "with ran as ( "\
    "select name_file,number,type_p,count(name_file) over (partition by type_p,name_file ) as ran from parameters join fileInf on parameters.id_p = fileInf.id_p where number <> 'conf') "\
    "select number from ran "\
    "where ran > 1 "\
    "order by name_file"
   )
    result = getSqldata(sqlite_select_query,cursor)
    return result
# получаем файлы которые были изменены в результате тестирования 
def getFileError(prav):
    sqlite_select_query =(
        "with db_file as (select name_file,sum_file_all from fileInf join md5sum_file on fileInf.id_file = md5sum_file.id_file "\
        "where fileInf.id_p = (select id_p from parameters where parav = '{p}') "\
        "order by name_file desc), "\
        "file as (select name_f,hs from analisis order by name_f desc), "\
        "all_analis as (select name_file,sum_file_all,name_f,hs from db_file join file on db_file.name_file = file.name_f) "\
        "select name_file from all_analis "\
        "where sum_file_all <> hs ".format(p=prav)
    )
    result = getSqldata(sqlite_select_query,cursor)
    return result


# Получить все элементы из БД
def getElementAll():
    sqlite_select_query = "select type_p,id_p,parav from parameters where number <> 'conf'"
    result = getSqldata(sqlite_select_query,cursor)
    return result
# Получить элементы по номеру из БД
def getElement(number):
    sqlite_select_query = "select type_p,id_p,parav from parameters where number = '{n}'".format(n=number)
    result = getSqldata(sqlite_select_query,cursor)
    return result
# Получаем список файлов по заданому правилу
def getFile(id_p):
    sqlite_select_query = "select name_file from fileInf where fileInf.id_p = {n}".format(n=id_p)
    result = getSqldata(sqlite_select_query,cursor)
    return result
#print(getElementAll())
# получаем глобальный параметр
def getGlobalParam():
    sqlite_select_query = "select * from global_param"
    result = getSqldata(sqlite_select_query,cursor)
    return result
#print(len(getGlobalParam()))
# получаем id_ правила 
def getIdPrav(prav):
    sqlite_select_query = "select id_p from parameters where parav = '{p}'".format(p=prav)
    result = getSqldata(sqlite_select_query,cursor)
    return result
# Запросы на добалвение записей в таблицы
# Добалвение во временную таблицу для анализа
def createAnalosis(f_hs):
    sqlite_insert_query = "INSERT INTO analisis (name_f,hs,stats) VALUES (?,?,?);"
    createData(sqlite_insert_query,f_hs,cursor,connect)
# глобальный параметр
def createGlobalParam(param):
    sqlite_insert_query = "INSERT INTO global_param (g_param) VALUES (?);"
    createData(sqlite_insert_query,param,cursor,connect)
#createGlobalParam([['gf.j',]])
def createPravilo(ogr):
    sqlite_insert_query = "INSERT INTO parameters (type_p,parav,number) VALUES (?,?,?);"
    createData(sqlite_insert_query,ogr,cursor,connect)
#createPravilo([('trt','do')])
def createHashFile(hash_file):
    sqlite_insert_query = "INSERT INTO md5sum_file (id_file,sum_file_all) VALUES (?,?);"
    createData(sqlite_insert_query,hash_file,cursor,connect)
def createHashStr(hash_file):
    sqlite_insert_query = "INSERT INTO md5sum_file (id_file,sum_file_str,num_str,sum_file_all) VALUES (?,?,?,?);"
    createData(sqlite_insert_query,hash_file,cursor,connect)
#createPravilo([('type_p','pravilo',"number_p")])
#createHashStr([123, '99dea2703097bbd0e301810618d7b0d3', '1', 'd41d8cd98f00b204e9800998ecf8427e'])
def createFile(param,type_p,pravilo,number_p):
    
    print("Добавление записей элемента {p} в БД ".format(p=pravilo))
    createPravilo([(type_p,pravilo,number_p)])
    #start_time = time.time()
    # получаем id  правила
    id_p = getParameters(pravilo)
    sqlite_insert_query = "INSERT INTO fileInf (name_file,id_p) VALUES (?,?);"
    i = 0
    sql_insert_param = []
    vr_cat = param[0][0]
    if type_p == 'l':
        sql_insert_param.append([param[0][0],id_p[0][0]])
    #print(param)
    while i < len(param):

            if type_p == 'l' and vr_cat != param[i][0]:
                sql_insert_param.append([param[i][0],id_p[0][0]])
                vr_cat = param[i][0]
            if type_p == 'd' or type_p == 'f':
                sql_insert_param.append([param[i][0],id_p[0][0]])
            i += 1
    createData(sqlite_insert_query,sql_insert_param,cursor,connect)
    #print("--- %s seconds ---" % (time.time() - start_time))
    
    i = 0
    arr_file_all = getFileAllPravilo(id_p[0][0])
    sql_insert_param.clear()
    #id_pr = getIdPrav(pravilo) #
    while i < len(param):
            #start_time = time.time()
            #print(param[i][0],pravilo)
            #indices = [(j, x.index(str(param[i][0]))) for j, x in enumerate(arr_file_all) if str(param[i][0]) in x]
            jj = 0
            while jj < len(arr_file_all):
                #print(arr_file_all[jj][1] == param[i][0])
                if arr_file_all[jj][1] == param[i][0]:
                    #print(arr_file_all[jj][0])
                    id_f = arr_file_all[jj][0]
                    del arr_file_all[jj]
                    break
                jj += 1
            #if len(indices) > 0:
            #print(arr_file_all[indices[0][0]][indices[0][1]-1])
            #id_f = getIdFile(param[i][0],id_pr[0][0])[0][0] #
            if type_p == 'l':
                #print(param)
                sql_insert_param.append([id_f,param[i][1],param[i][2],param[i][3]])
            else:
                sql_insert_param.append([id_f,param[i][1]])
            #print("--- %s seconds1 ---" % (time.time() - start_time))
            i += 1
    
    #print("Добавление хэш суммы после циклов")
    if type_p == 'l' and len(sql_insert_param) > 0:
        #print(sql_insert_param)
        createHashStr(sql_insert_param)
    if type_p != 'l' and len(sql_insert_param) > 0:
        createHashFile(sql_insert_param)
# Удаление данных
def deleteTableAllData(table_name):
    sqlite_delete_query = "DELETE FROM " +table_name
    delteData(sqlite_delete_query,cursor,connect)
#deleteTableAllData('fileInf')

