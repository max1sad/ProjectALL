import datetime as DT
import DBConection
import read_conf
# устанавливаем соединение с БД
dbname = read_conf.read_file("DBOTRS","dbname")
user = read_conf.read_file("DBOTRS","user")
host = read_conf.read_file("DBOTRS","host")
password = read_conf.read_file("DBOTRS","password")
port = read_conf.read_file("DBOTRS","port")
connetction = DBConection.create_connection(dbname,user,password,host,port)
# Получаем Максимальный id заявки нужно при первом запуске.
def get_max_id_ticket():
    sql="select max(id) as id from ticket where ticket_state_id = 1"
    max_id_ticket = DBConection.execute_read_query(connetction,sql)
    return max_id_ticket
#print(get_max_id_ticket()[0][0])
# Получаем все новые заявки от предыдущих расмотренных заявок.
def get_new_ticket_in_group(max_ticket):
    sql = ("select name,tn from ticket inner join queue "
    "on ticket.queue_id = queue.id "
    "where ticket_state_id = 1 and ticket.id > " + str(max_ticket) +";"
    )
    new_ticket = DBConection.execute_read_query(connetction,sql)
    return new_ticket
#print(len(get_new_ticket_in_group(2)))
#Проверка наличия в БД пользователя
def check_client_tg(id_tg):
    select_id_tg = "SELECT id FROM public.customer_user where mobile = '" + str(id_tg) +"';"
    check_client = DBConection.execute_read_query(connetction,select_id_tg)
    return len(check_client)
#добавление пользователя в БД otrs 
def create_customer(data_customer):
    
    date_check = DT.datetime.now()
    dat = date_check.strftime('%Y-%m-%d %H:%M:%S')
    dt = data_customer[1].split()
    # создаем словать как обьект таблицы
    customer_user = dict(login=data_customer[0],email=data_customer[0],customer_id=data_customer[0],
                        first_name=dt[0],last_name=dt[1],mobile=data_customer[2],create_time=dat,change_time=dat,
                         valid_id=1,create_by=1,change_by=1)
    default_data = list(customer_user.values())
    post_records = ", ".join(["%s"] * len(default_data))
    insert_customer = (
        f"INSERT INTO public.customer_user(login, email, customer_id, first_name, last_name, "
        f"mobile, create_time, change_time, valid_id, create_by, change_by) VALUES ({post_records});"
    )
    DBConection.add_query(connetction,default_data,insert_customer)
        
#create_customer(['maxim_test_un@mail.ru','Максим Баранов','77232342'])
    #return 0
# получение пользователя из БД otrs по id телеграмм
def get_customer(id_tg):
    select_id_client = "SELECT first_name, last_name FROM public.customer_user where mobile = '" + str(id_tg) +"';"
    return DBConection.execute_read_query(connetction,select_id_client)
#print(get_customer("ffuuu19@hotmail.com"))
# получаем mail клиента
def get_customer_mail(id_tg):
    select_id_client = "SELECT email FROM public.customer_user where mobile = '" + str(id_tg) +"';"
    return DBConection.execute_read_query(connetction,select_id_client)
# получаем id очереди
def get_id_queue(name_queue):
    select_sql = "SELECT id FROM public.queue where name = '" + str(name_queue) +"';"
    return DBConection.execute_read_query(connetction,select_sql)
#print(len(get_id_queue("КП СГП1")))
def get_tn_max():
    select_sql = "select tn from public.ticket order by id desc limit 1"
    return DBConection.execute_read_query(connetction,select_sql)
def get_count_mail(mail):
    select_sql = "select count(*) as co_mail from public.customer_user where email = '" + str(mail) + "'"
    return DBConection.execute_read_query(connetction,select_sql)
def update_customer_mail(mail,id_tg):
    list_dat = []
    list_dat.append(str(mail))
    update_sql = (
        f"update public.customer_user SET mobile =  '{str(id_tg)}'  where email = %s"
    )
    DBConection.add_query(connetction,list_dat,update_sql)
#update_customer_mail('Nikitayasenkov@mail.ru',123456775)
#print(get_count_mail('maxim_test_un@mail.ru')[0][0])
def create_ticket(tn,unix,dat,queue,mail):
    
    ticket = dict(tn=str(tn),title="Telegram Bot",queue_id=queue,customer_id=mail,
                  customer_user_id=mail,create_time_unix=unix,create_time=dat,
                  change_time=dat,ticket_priority_id=3,ticket_lock_id=1,
                  type_id=1,user_id=1,responsible_user_id=1,
                  ticket_state_id=1,create_by=1,change_by=1,timeout=0,
                  until_time=0,escalation_time=0,escalation_update_time=0,
                  escalation_response_time=0,escalation_solution_time=0,archive_flag=0)
    list_data = list(ticket.values())
 
    post_records = ", ".join(["%s"] * len(list_data))
    #print(post_records)
    
    insert_ticket = (
    f"INSERT INTO public.ticket(tn, title, queue_id, customer_id, customer_user_id," 
        f"create_time_unix, create_time, change_time, ticket_priority_id, ticket_lock_id, type_id, user_id, responsible_user_id," 
        f"ticket_state_id,  create_by, change_by, timeout, until_time, escalation_time, escalation_update_time, escalation_response_time," 
        f"escalation_solution_time, archive_flag) VALUES ({post_records});"
    )
    #print(list_data)
    DBConection.add_query(connetction,list_data,insert_ticket)
    #print(insert_ticket)
def get_id_ticket(tn):
    select_sql = "select id from public.ticket where tn = '" + str(tn) +"';"
    return DBConection.execute_read_query(connetction,select_sql)
def get_article_id(id_ticket):
    select_sql = "select id from public.article where ticket_id = " + str(id_ticket) +";"
    return DBConection.execute_read_query(connetction,select_sql)
# обавление в таблицу ticket_flag
def create_ticket_flag(ticket_id,create_time):
   ticket_flag = dict(ticket_id=int(ticket_id),ticket_key="Seen",ticket_value="1",create_time=create_time,create_by=1)
   list_data = list(ticket_flag.values())
 
   post_records = ", ".join(["%s"] * len(list_data))
   insert_ticket_flag = (
   f"INSERT INTO public.ticket_flag(ticket_id, ticket_key, ticket_value, create_time, create_by) VALUES ({post_records});"
   )
   DBConection.add_query(connetction,list_data,insert_ticket_flag)
def create_article(ticket_id,a_from,a_to_group,a_subject,a_body,unux,dat_full,dat):

    article = dict(ticket_id=ticket_id,article_type_id=8,article_sender_type_id=3,
                   a_from=a_from,a_to=a_to_group,a_subject=a_subject,a_content_type="text/plain; charset=utf-8",a_body=a_body,
                   incoming_time=unux,content_path=dat,valid_id=1,create_time=dat_full,
                   create_by=1,change_time=dat_full,change_by=1)
    list_data = list(article.values())
    
  
    post_records = ", ".join(["%s"] * len(list_data))

    insert_article = (
    f"INSERT INTO public.article("
            f"ticket_id, article_type_id, article_sender_type_id, a_from," 
            f"a_to, a_subject, a_content_type, a_body, incoming_time," 
            f"content_path, valid_id, create_time, create_by, change_time," 
            f"change_by) VALUES ({post_records});"
    )
    DBConection.add_query(connetction,list_data,insert_article)
def create_article_flag(id_article,dat_full):
    article_flag = dict(article_id=id_article, article_key="Seen", article_value="1", create_time=dat_full, create_by=1)
    list_data = list(article_flag.values())
   
    post_records = ", ".join(["%s"] * len(list_data))
    insert_ticket_flag = (
        f"INSERT INTO public.article_flag("
            f"article_id, article_key, article_value, create_time, create_by) VALUES ({post_records});"
    )
    DBConection.add_query(connetction,list_data,insert_ticket_flag)
def create_ticket_history(str1_name,str2_name,str3_name,ticket_id,article_id,queun_id,dat_full):
    
    ticket_history = dict(name=str2_name, history_type_id=1, ticket_id=ticket_id, type_id=1, queue_id=queun_id,
                          owner_id=1, priority_id=3, state_id=1, create_time=dat_full, create_by=1, change_time=dat_full,
                          change_by=1)
    list_data = list(ticket_history.values())
  
    post_records = ", ".join(["%s"] * len(list_data))

    insert_ticket_history = (
        f"INSERT INTO public.ticket_history("
            f"name, history_type_id, ticket_id, type_id, queue_id," 
            f"owner_id, priority_id, state_id, create_time, create_by, change_time," 
            f"change_by) VALUES ({post_records});"
    )
    DBConection.add_query(connetction,list_data,insert_ticket_history)
    ticket_history["name"] = str3_name
    ticket_history["history_type_id"] = 21
    list_data. clear()
    list_data = list(ticket_history.values())
    #list_data[0] = str3_name
    #list_data[1] = 21
    DBConection.add_query(connetction,list_data,insert_ticket_history)
    ticket_history["name"] = str1_name
    ticket_history["history_type_id"] = 29
    ticket_history["article_id"] = article_id
    list_data. clear()
    list_data = list(ticket_history.values())
    #[0] = str1_name
    #list_data[1] = 29
    #list_data.append(article_id)
    post_records = ", ".join(["%s"] * len(list_data))
    insert_ticket_history_art = (
        f"INSERT INTO public.ticket_history("
            f"name, history_type_id, ticket_id, type_id, queue_id," 
            f"owner_id, priority_id, state_id, create_time, create_by, change_time," 
            f"change_by, article_id) VALUES ({post_records});"
    )
    DBConection.add_query(connetction,list_data,insert_ticket_history_art)
def create_article_attachment(attachement,id_article, dat_full):
    article_attachment= dict(content="",content_size="",filename="",
                             article_id=id_article, create_time=dat_full, change_time=dat_full, content_type="image/jpeg",
                             disposition="attachment",  create_by=1, change_by=1)
    article_attachment.update(attachement)
    list_data = list(article_attachment.values())
  
    post_records = ", ".join(["%s"] * len(list_data))
    insert_article_attachment = (
        f"INSERT INTO public.article_attachment("
            f"content, content_size, filename, article_id, create_time, change_time, content_type, disposition,   create_by, change_by) "
            f"VALUES ({post_records});"
    )

    DBConection.add_query(connetction,list_data,insert_article_attachment)
    #return 0
def create_article_flag_bot(id_ticket):
    d = dict(ticket_id=id_ticket,flag="no")
    post_records = ", ".join(["%s"] * len(d))
    insert_flag_bot = (
        f"insert into public.articke_flag_bot (ticket_id, flag) values ({post_records})"
    )
    list_data = list(d.values())
    DBConection.add_query(connetction,list_data,insert_flag_bot)
#create_article_flag_bot(36)

# общий метод для хранения данных для создания заявки, так как требуется много таблиц, и разные данные
def full_request(list_inf,id_client):
    date_check = DT.datetime.now()
    dat_full = date_check.strftime('%Y-%m-%d %H:%M:%S')
    dat = date_check.strftime('%Y/%m/%d')
    dat1 = DT.datetime.strptime(dat_full,'%Y-%m-%d %H:%M:%S')
    unix1 = str(dat1.timestamp())
    unix = int(unix1[0:len(unix1)-2])
    #print(dat)
    #print(date_check.strftime('%Y%m%d'))
    tn_end = get_tn_max()[0][0]
    queue = get_id_queue(list_inf[0])[0][0]
    mail = get_customer_mail(id_client)[0][0]
    tn = date_check.strftime('%Y%m%d') + str(int(tn_end[8:len(tn_end)]) + 5)
    create_ticket(tn,unix,dat_full,queue,mail)
    id_ticket = get_id_ticket(tn)[0][0]
    #print("id_ticket "+ str(id_ticket))
    create_ticket_flag(id_ticket,dat_full)

    full_name = get_customer(id_client)
    a_from = f"\"{full_name[0][0]} {full_name[0][1]}\" <{mail}>"
    create_article(id_ticket, a_from, list_inf[0], "Telegram Bot", list_inf[1], unix, dat_full, dat)
    id_article = get_article_id(id_ticket)[0][0]
    create_article_flag(id_article, dat_full)
    str1_name_ticket = "%%"
    str2_name_ticket = f"%%{tn}%%{list_inf[0]}%%3 normal%%new%%{id_ticket}"
    str3_name_ticket = f"%%CustomerID={mail};CustomerUser={mail};"
    create_ticket_history(str1_name_ticket, str2_name_ticket, str3_name_ticket, id_ticket, id_article, queue, dat_full)
    create_article_flag_bot(id_ticket)
    out_id = dict(
        id=id_article,data_f=dat_full
    )
    return out_id
    #if len(attachenmt) > 1:
    #    create_article_attachment(attachenmt,id_article,dat_full)

def get_id_ticket_out():
    select_sql = (f"with count_article as (select ticket_id, count(ticket_id) as count from public.article "
                    f"group by ticket_id order by ticket_id desc) "
                    f"select distinct ticket_id from count_article where count >= 2 and ticket_id in "
                    f"(select ticket_id from public.articke_flag_bot where flag = 'no')"
    )
    return DBConection.execute_read_query(connetction,select_sql)

def get_article_input_out_ticket_id():
    select_sql = (f"with count_article as (select ticket_id, count(ticket_id) as count from public.article "
                    f"group by ticket_id order by ticket_id desc), "
                    f"id_ticket as (select ticket_id from count_article where count >= 2 and ticket_id in "
                    f"(select ticket_id from public.articke_flag_bot where flag = 'no'))"
                    f"select mobile from public.customer_user where email in (select customer_user_id from id_ticket inner join public.ticket " 
                    f"on id_ticket.ticket_id = public.ticket.id)"
    )
    return DBConection.execute_read_query(connetction,select_sql)
#print(get_article_input_out_ticket_id())
def update_article_flag_bot(id_ticket):
    list_id = []
    if len(id_ticket) >= 1:
        for id_tick in id_ticket:
            #print("update")
            list_id.append(int(id_tick[0]))
            #print(list_id)
            update_sql = (
                f"update public.articke_flag_bot SET flag = 'yes' where ticket_id = %s"
            )
            DBConection.add_query(connetction,list_id,update_sql)
            list_id.clear()

def create_user_check(id_client,m_text):
    d = dict(user_id=id_client,m_photo=str(m_text),id_input_menu="1")
    post_records = ", ".join(["%s"] * len(d))
    insert_user_sql = (
                f"INSERT INTO public.check_user(user_id, m_photo, id_input_menu)"
                    f"VALUES ({post_records});"
            )
    list_data = list(d.values())
    DBConection.add_query(connetction,list_data,insert_user_sql)
def get_user_bot(id_client):
    select_sql = (
        f"select count(*) as c from public.check_user where user_id = '" + str(id_client) + "';"
    )
    return DBConection.execute_read_query(connetction,select_sql)
def get_user_message_bot(id_client):
    select_sql = (
        f"select m_photo from public.check_user where user_id = '" + str(id_client) + "';"
    )
    return DBConection.execute_read_query(connetction,select_sql)
def get_user_menu_bot(id_client):
    select_sql = (
        f"select id_input_menu from public.check_user where user_id = '" + str(id_client) + "';"
    )
    return DBConection.execute_read_query(connetction,select_sql)

def update_user_bot_message(id_client,m_text):
    d = dict(m_photo=str(m_text))
    list_data = list(d.values())
    update_sql = (
                f"update public.check_user SET m_photo = %s where user_id = '" + str(id_client) + "';"
            )
    DBConection.add_query(connetction,list_data,update_sql)
def update_user_bot_menu(id_client,m_text):
    d = dict(id_input_menu=str(m_text))
    list_data = list(d.values())
    update_sql = (
                f"update public.check_user SET id_input_menu = %s where user_id = '" + str(id_client) + "';"
            )
    DBConection.add_query(connetction,list_data,update_sql)
def delete_user_bot(id_client):
    delete_sql = (
        f"DELETE FROM public.check_user WHERE user_id = '" + str(id_client) +"';"
    )
    DBConection.delete_item(connetction,delete_sql)
#delete_user_bot("22342342")
#update_user_bot_menu("22342342","2")
#print(get_user_menu_bot("22342342")[0][0] == "1")
#update_user_bot_message("22342342",get_user_message_bot("22342342")[0][0]+"\nпроверка")
#print(get_user_message_bot("22342342")[0][0])
#print(get_user_bot("22342342")[0][0] == 1)
#create_user_check("22342342","проверка")
#list_teg = ["Product","Message"]
#list_inf = chekFile.read_file_out_text("./filechek", list_teg, "772376797")
#print(list_inf[0])
#str1_name_ticket = "%%"
#print(str1_name_ticket)
#print(get_article_id(13)[0][0])
#full_request(list_inf, "772376797")
#if len(get_article_input_out_ticket_id()) >= 1:
#    print("ok")
#for rr in get_article_input_out_ticket_id():
#    print(rr[0])
#update_article_flag_bot(get_id_ticket_out())


