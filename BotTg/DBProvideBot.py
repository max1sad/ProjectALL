import datetime as DT
import DBConnectBot
import modelAllUser
import sys
import read_conf
# устанавливаем соединение с БД
dbname = read_conf.read_file("DBBOT","dbname")
user = read_conf.read_file("DBBOT","user")
host = read_conf.read_file("DBBOT","host")
password = read_conf.read_file("DBBOT","password")
port = read_conf.read_file("DBBOT","port")
connetction = DBConnectBot.create_connection_bot(dbname,user,password,host,port)
def connection_test():
    if  connetction == 0:
        sys.exit()
#if  connetction == 0:
#    sys.exit()
# запросы на выборку данных

# проверка существует ли пользователь, возврат количества
def b_get_user(id_client):
    select_sql = (
        f"select count(*) as c from public.check_user where id_user = '" + str(id_client) + "';"
    )
    return DBConnectBot.execute_read_query_bot(connetction,select_sql)
#print(b_get_user("123"))

def b_get_all_user(id_client):
    all_user_dict = dict(
        id_user="", time_start="",id_registration="", name_famyli="", mail="", id_product="", product_name="", 
            message_time="", message_product="", id_support="", message_support="", id_zayvaka=""
    )
    select_sql = (
        f"select * from public.check_user where id_user = '" + str(id_client) + "';"
    )
    i = 0
    sql_result = DBConnectBot.execute_read_query_bot(connetction,select_sql)
    if len(sql_result) == 1:
        for key_dict in all_user_dict:
            #print(key_dict)
            all_user_dict[key_dict] = sql_result[0][i]
            i += 1
    #print(len(DBConnectBot.execute_read_query_bot(connetction,select_sql)[0]))
    return all_user_dict
#print(b_get_all_user("123"))
# получаем все файлы которые загрузил пользователь
def b_get_file_name_on_user(id_client):
    select_sql = (
        f"select  distinct name_file from public.check_user_file where name_file  in ( "
        f"select name_file from public.check_user_file where id_user = '" + str(id_client) + "' order by message_time desc limit 5);"
    )
    return DBConnectBot.execute_read_query_bot(connetction,select_sql)
#print(b_get_file_name_on_user("772376797"))
def b_get_count_file(id_client):
    select_sql = (
        f"select count(*) from check_user_file where id_user = '" + str(id_client) + "' group by id_user;"
    )
    return DBConnectBot.execute_read_query_bot(connetction,select_sql)
#if not b_get_count_file("484433331"):
#    print("ok")
# получаем максимальное время загруженного файла, где имеется подпись
def b_get_file_time_max_and_text(id_client):
    select_sql = (
        f"select MAX(message_time) as max_f from public.check_user_file where id_user = '" + str(id_client) + "' " 
            f"and message_for_file <> 'None' group by id_user;"
    )
    return DBConnectBot.execute_read_query_bot(connetction,select_sql)
def b_get_file_text(id_client,time_file):
    select_sql = (
        f"select message_for_file from public.check_user_file where id_user = '" + str(id_client) + "' " 
            f"and message_time = '" + str(time_file) + "';"
    )
    return DBConnectBot.execute_read_query_bot(connetction,select_sql)

def b_get_time_is_over():
    select_sql = (
        f"select id_user, time_start from public.check_user"
    )
    return DBConnectBot.execute_read_query_bot(connetction,select_sql)

#print(b_get_file_time_max_and_text("772376797")[0][0])
#print(b_get_file_text("772376797",b_get_file_time_max_and_text("772376797")[0][0]))
# запросы на удаление данных
def b_delete_user(id_client):
    delete_sql = (
        f"DELETE FROM public.check_user WHERE id_user = '" + str(id_client) +"';"
    )
    DBConnectBot.delete_item_bot(connetction,delete_sql)

def b_delete_file(id_client):
    delete_sql = (
        f"DELETE FROM public.check_user_file WHERE id_user = '" + str(id_client) +"';"
    )
    DBConnectBot.delete_item_bot(connetction,delete_sql)
#b_delete_user("123")

# запросы на обновление данных

def b_update_table(id_client,name_item,item_data):
    list_data = [item_data]
    update_sql = (
        f"update public.check_user SET " + name_item + " = %s where id_user = '" + str(id_client) + "';"
    )
    DBConnectBot.add_query_update_bot(connetction,list_data,update_sql)

#b_update_table("123","name_famyli","rewrwe")
# запросы на добавление данных
# На добавление информации о картинке
def b_create_photo_on_user(id_client,file_name,message_text):
    date_now = DT.datetime.now()
    dat = date_now.strftime('%H:%M:%S.%f')
    if message_text == None:
        message_text = "None"
    file_info = dict(
        id_user=str(id_client),name_file=file_name,message_for_file=str(message_text),message_time=str(dat)
    )
    post_records = ", ".join(["%s"] * len(file_info))
    insert_file = (
        f"INSERT INTO public.check_user_file("
            f"id_user, name_file, message_for_file, message_time) VALUES ({post_records});"
    )
    list_data = list(file_info.values())
    DBConnectBot.add_query_update_bot(connetction,list_data,insert_file)

def b_create_user_start(id_client):
    date_now = DT.datetime.now()
    dat = date_now.strftime('%Y-%m-%d %H:%M:%S')
    all_user_dict = dict(
        id_user=str(id_client), time_start=str(dat)
    )
    post_records = ", ".join(["%s"] * len(all_user_dict))
    insert_user = (
        f"INSERT INTO public.check_user("
            f"id_user, time_start) VALUES ({post_records});"
    )
    list_data = list(all_user_dict.values())
    DBConnectBot.add_query_update_bot(connetction,list_data,insert_user)
#b_create_user_start("12334")
#ob_name = modelAllUser.field()
#print(ob_name.id_user())
#all_u = b_get_all_user("123")
#print(len(b_get_file_name_on_user("123")))
#b_update_table("123",ob_name.id_registration(),3)
#print(b_get_all_user("123").get(ob_name.id_registration()) == 3)
#b_update_table("123",ob_name.id_registration(),4)
#print(b_get_all_user("123").get(ob_name.id_registration()) == 4)