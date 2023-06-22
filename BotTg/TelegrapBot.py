import telebot
from telebot import types
from datetime import datetime
import datetime as DT
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading
import time
import sys
import os
import DBProvideBot
import DBProvide
import modelAllUser
import reg_ex
import encode_file
import logger
import read_conf
import ticket_new
# указываем токен подключения к боту, вынести в файл.
token = read_conf.read_file("BOT","token")
arm_abi = read_conf.read_file("PRODUCT","armabi")
nabat = read_conf.read_file("PRODUCT","nabat")
kp_sgp = read_conf.read_file("PRODUCT","kpsgp")
telegram = read_conf.read_file("PRODUCT","telegram")
c_nabat = read_conf.read_file("CHAT","c_nabat")
c_armabi = read_conf.read_file("CHAT","c_armabi")
dirname = os.path.dirname(__file__)
count_connection_token = 0
gg = 0
# проверка если не задан токен телеграмм
if token == 0:
    sys.exit()
# проверка существуют ли заданные продукты в БД otrs
if nabat != 0 and len(DBProvide.get_id_queue(nabat)) == 0:
    logger.file_log(f"В БД не найдена очередь {nabat}")
    quit()
elif nabat == 0:
    logger.file_log(f"В конфигурационном файле не найдена очередь")
    quit()
if arm_abi != 0 and len(DBProvide.get_id_queue(arm_abi)) == 0:
    logger.file_log(f"В БД не найдена очередь {arm_abi}")
    quit()
elif arm_abi == 0:
    logger.file_log(f"В конфигурационном файле не найдена очередь")
    quit()
if kp_sgp != 0 and len(DBProvide.get_id_queue(kp_sgp)) == 0:
    logger.file_log(f"В БД не найдена очередь {kp_sgp}")
    quit()
elif kp_sgp == 0:
    logger.file_log(f"В конфигурационном файле не найдена очередь")
    quit()
if telegram != 0 and len(DBProvide.get_id_queue(telegram)) == 0:
    logger.file_log(f"В БД не найдена очередь {telegram}")
    quit()
elif telegram == 0:
    logger.file_log(f"В конфигурационном файле не найдена очередь")
    quit()

bot = telebot.TeleBot(token)
Ob = modelAllUser.field()
# Проверка подключения к БД, если что, не выполняем программу дальше
#DBProvideBot.connection_test()
#  проверка ответа на заявку в БД по таймеру, оповещение клиента об ответе
def check_db_time():
    threading.Timer(120.0,check_db_time).start()
    id_telegram = DBProvide.get_article_input_out_ticket_id()
    if id_telegram != None and len(id_telegram) >= 1:
        for id_tg in id_telegram:
            try:
                bot.send_message(int(id_tg[0]),"Ответ специалиста по вашему запросу отправлен на адрес электронной почты, указанный при регистрации ",parse_mode='Markdown')
            except:
                #print(f"ошибка при отправке сообщения пользователю  {id_tg}")
                logger.file_log(f"ошибка при отправке сообщения пользователю  {id_tg}")

        DBProvide.update_article_flag_bot(DBProvide.get_id_ticket_out())

check_db_time()

# удаление пользователей которые не завершили действия спустя 1 день
def delere_user_day():
    threading.Timer(600.0,delere_user_day).start()
    time_over = DBProvideBot.b_get_time_is_over()
    i = 0
    if time_over != None:
        while i < len(time_over):
        
            dat = datetime.now()
            dat_difference = dat - datetime.strptime(time_over[i][1], "%Y-%m-%d %H:%M:%S")
            dat_difference_list = str(dat_difference).split(',')
            if len(dat_difference_list) == 2:
                dat_day = dat_difference_list[0].split(' ')
                if int(dat_day[0]) >= 1:
                    DBProvideBot.b_delete_user(time_over[i][0])
                    DBProvideBot.b_delete_file(time_over[i][0])
                dat_difference_list.clear()
                dat_day.clear()
            i += 1

delere_user_day()
# Оповещение Администраторов о новых заявках
def alert_admin():
    threading.Timer(300.0,alert_admin).start()
    if c_nabat != 0 and c_armabi !=0:
        arr_group = ticket_new.ticket()
        if arr_group:
            i = 0
            while i < len(arr_group):
                if ((arr_group[i][0].lower().find("АРМ".lower())) >= 0) or \
                ((arr_group[i][0].lower().find("СГП".lower())) >= 0):
                    try:
                        bot.send_message(c_armabi,f"Новая заявка в очереди: {arr_group[i][0]}; Номер заявки: {arr_group[i][1]} ",parse_mode='Markdown')
                    except Exception as e:
                        logger.file_log(f"Ошибка отправки в группу: id_g {c_armabi} ")
                if ((arr_group[i][0].lower().find("Набат".lower())) >= 0):
                    try:
                        bot.send_message(c_armabi,f"Новая заявка в очереди: {arr_group[i][0]}; Номер заявки: {arr_group[i][1]} ",parse_mode='Markdown')
                    except Exception as e:
                        logger.file_log(f"Ошибка отправки в группу: id_g {c_nabat} ")
                i = i + 1 
alert_admin()
# первое сообщение пользователя должно быть /start
@bot.message_handler(commands=['start','exit','newchatid'])
def start(message):
    id_client = message.from_user.id
    # Проверяем вызов команды /newchatid для определения данных для новой группы 
    if message.text == '/newchatid':
        # Пишем в лог данные новой группы
        #print(f"ID: {str(message.chat.id)}  Name: {message.chat.title}")
        logger.file_log(f"id_g: {str(message.chat.id)}  name_g: {message.chat.title}")

    if str(id_client) == str(message.chat.id):   
        delete_users(id_client)
    
    
def delete_users(id_client):
    # проверяем имеется ли такой пользователь в БД, удалем.
    if DBProvideBot.b_get_user(id_client)[0][0] == 1:
        DBProvideBot.b_delete_user(id_client)
        DBProvideBot.b_delete_file(id_client)
    # стартовое меню.
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Задать вопрос")
    markup.add(btn1)
    bot.send_message(id_client, "Бот тех. поддержки РусБИТех на связи",reply_markup=markup)

# функция определяет что отправлена картинка была.
@bot.message_handler(content_types=['photo','document'])
def image_check(message):
    # проверяем что сообщение не из групп в которых бот состоит 
    if str(message.from_user.id) == str(message.chat.id):
        id_client = message.from_user.id
        # Проверяем что выбрали уже продукт
        if DBProvideBot.b_get_all_user(id_client).get(Ob.id_product()) == 2:
            if message.content_type == 'document':
                bot.send_message(message.from_user.id,"Запрос может содержать только сжатые изображения",parse_mode='Markdown')
            if message.content_type == 'photo':
                file_id = message.photo[-1].file_id
                file_info = bot.get_file(file_id)
                
                if file_info.file_size < 1000000:
                    #download_file = bot.download_file(file_info.file_path)
                    if not not DBProvideBot.b_get_count_file(id_client):
                        if DBProvideBot.b_get_count_file(id_client)[0][0] < 6:   
                            DBProvideBot.b_create_photo_on_user(id_client,file_info.file_path,message.caption)
                            #bot.send_message(message.from_user.id,f"Завершить заявку ?",
                            #             reply_markup=test_gg(message))
                            #bot.edit_message_reply_markup(message.chat.id, message_id = message.message_id-1, reply_markup = '')# удаляем кнопки у последнего сообщения
                            #bot.delete_message(message.chat.id, message.message_id-1)

                            if message.caption != None:
                                #logger.file_log("Из основного")
                                copy_text_on_file(id_client)     
                    else:
                            DBProvideBot.b_create_photo_on_user(id_client,file_info.file_path,message.caption)
                            if message.caption != None:
                                #logger.file_log("Из основного1")
                                copy_text_on_file(id_client)
                            bot.send_message(message.from_user.id,f"Для завершения нажмите",
                                        reply_markup=test_gg(message))
                            #try:
                            #bot.edit_message_reply_markup(message.chat.id, message_id = message.message_id-1, reply_markup = '')# удаляем кнопки у последнего сообщения
                            #bot.delete_message(message.chat.id, message.message_id-1)
                            #except Exception as e:
                            #    print(f"{e} -- error")
 
                        

# загрузка файлов из сообщений клиента на сервер, для дальнейшего кодирования данных файлов.
def download_file(file_name_down):
        if len(file_name_down) != 0:
            i = 0
            while i < len(file_name_down):
                download_file = bot.download_file(file_name_down[i][0])
                # сохраняем на сервер временно, что бы закодировать, и получить доп инфу по файлу.
                with open(f"{dirname}/{file_name_down[i][0]}","wb") as new_file:
                    new_file.write(download_file)
                i += 1


# главная функция, для работы с сообщениями
@bot.message_handler(content_types=['text'])
# меню для авторизованного пользователя
def get_messages_all(message):
    if c_nabat != str(message.chat.id) and c_armabi != str(message.chat.id):
        check_mess = 0
        id_client = message.chat.id
        # Выйти в главное меню
        if message.text == '/exit':
            check_mess = 1
            start(message) 

        # проверяем какой пункт меню выбрали
        if message.text == 'Задать вопрос':
            check_mess = 1
            # проверяем имеется ли такой пользователь, если уже есть, то удаляем и по новой создаем как новую сессию
            if DBProvideBot.b_get_user(id_client)[0][0] == 0:
                DBProvideBot.b_create_user_start(id_client)
                DBProvideBot.b_update_table(id_client,Ob.id_product(),1)
            else:
                DBProvideBot.b_delete_user(id_client)
                DBProvideBot.b_create_user_start(id_client)
                DBProvideBot.b_update_table(id_client,Ob.id_product(),1)
        
                
        
        # подача заявки зарегистрирвоанным пользователем 1-2 вывод меню с выбором продукта
        if DBProvide.check_client_tg(id_client) >= 1 and DBProvideBot.b_get_all_user(id_client).get(Ob.id_product()) == 1 and \
                DBProvideBot.b_get_all_user(id_client).get(Ob.id_support()) != 1:
            check_mess = 1
            client_name = DBProvide.get_customer(id_client)
            bot.send_message(message.from_user.id,
                            f"Здравствуйте, {client_name[0][0]}!\n"
                            f"Запрос может содержать до 5 изображений, каждое не более 10 МБ",reply_markup=menu_exit_client(message))
            DBProvideBot.b_update_table(id_client,Ob.id_product(),2)
            menu_for_product(message)

        # получаем сообщение для обращения в поддержку
        #logger.file_log(str(DBProvideBot.b_get_all_user(id_client).get(Ob.id_support())))
        if message.text != '/support' and DBProvideBot.b_get_all_user(id_client).get(Ob.id_support()) == 1 and \
                message.text != '✅ Отправить':
            check_mess = 1
            list_data = [DBProvideBot.b_get_all_user(id_client).get(Ob.product_name()),
                                            str(message.text)]
            DBProvide.full_request(list_data, id_client)
            bot.send_message(message.from_user.id,"Ваша заявка зарегистрирована, ответ поступит в течении 3-х рабочих дней",parse_mode='Markdown')
            start(message)

        # подача заявки в поддержку
        if message.text == '/support':
            check_mess = 1
            # проверяем имеется ли такой пользователь, если уже есть, то удаляем и по новой создаем как новую сессию
            if DBProvideBot.b_get_user(id_client)[0][0] == 0:
                DBProvideBot.b_create_user_start(id_client)
            else:
                DBProvideBot.b_delete_user(id_client)
                DBProvideBot.b_create_user_start(id_client)

            if DBProvide.check_client_tg(id_client) != 0:
                DBProvideBot.b_update_table(id_client,Ob.id_support(),1)
                DBProvideBot.b_update_table(id_client,Ob.product_name(),telegram)
                bot.send_message(message.from_user.id,"Опишите проблему, связанную с учетными данными",parse_mode='Markdown')
            else:
                bot.send_message(message.from_user.id,"Пройдите регистрацию",parse_mode='Markdown') 

        # регистрация пользователя в системе otrs
        if DBProvide.check_client_tg(id_client) == 0 and DBProvideBot.b_get_user(id_client)[0][0] != 0:
            check_mess = 1
            registration_user(message,id_client)
        # получаем сообщение которое вводилось в качестве вопроса, обьединяем несколько сообщений в одно.
        if DBProvideBot.b_get_all_user(id_client).get(Ob.id_product()) == 2 and\
            DBProvideBot.b_get_all_user(id_client).get(Ob.product_name()) != None:
            check_mess = 1

            if message.text != '✅ Отправить' and message.text != '/support' and message.text != '/exit':
                    date_now = DT.datetime.now()
                    dat = date_now.strftime('%H:%M:%S.%f')
                    if  DBProvideBot.b_get_all_user(id_client).get(Ob.message_product()) != None:
                        DBProvideBot.b_update_table(id_client,Ob.message_product(),
                                    DBProvideBot.b_get_all_user(id_client).get(Ob.message_product()) +"\n"+ str(message.text))
                        bot.send_message(message.from_user.id,f"Для завершения нажмите",
                                        reply_markup=test_gg(message))
                        try:
                            bot.edit_message_reply_markup(message.chat.id, message_id = message.message_id-1, reply_markup = '')# удаляем кнопки у последнего сообщения
                            bot.delete_message(message.chat.id, message.message_id-1)
                        except Exception as e:
                            logger.file_log(f"Ошибка удаления кнопки: {e}")
                    else:

                        DBProvideBot.b_update_table(id_client,Ob.message_product(),str(message.text))
                        bot.send_message(message.from_user.id,f"Для завершения нажмите",
                                        reply_markup=test_gg(message))
                        
                    DBProvideBot.b_update_table(id_client,Ob.message_time(),str(dat))
                    #print(dat)

        # оправка только для текстовой заявки
        if (message.text == '✅ Отправить' and DBProvideBot.b_get_all_user(id_client).get(Ob.message_product())) or\
            (message.text == '✅ Отправить' and len(DBProvideBot.b_get_file_name_on_user(id_client)) != 0):

            create_ticket(id_client,message)
    
        # проверяем если ввели текст, и он не соответствует не какому из действий
        if check_mess == 0:
            bot.send_message(message.from_user.id,"Для вызова меню введите /start",parse_mode='Markdown')

def registration_user(message,id_client):
        # Пользователя нет в системе otrs, первичная регистрация, поле id_registration от None до 3(уже не включено)
    if DBProvide.check_client_tg(id_client) == 0 and DBProvideBot.b_get_user(id_client)[0][0] == 1:
        check_mess = 1
        # проверка подтверждения операции, если такой адрес почты уже имеется в системе, сменил номер телефона когда
        if message.text == 'Нет':
            start(message)
            #return
        if message.text == 'Да':
            DBProvide.update_customer_mail(DBProvideBot.b_get_all_user(id_client).get(Ob.mail()),id_client)
            DBProvideBot.b_update_table(id_client,Ob.id_registration(),3)
            bot.send_message(id_client,"Регистрация прошла успешно!!!",parse_mode='Markdown')
            start(message)

        # 3- получаем адрес электронной почты, проверяем его корректность        
        if DBProvideBot.b_get_all_user(id_client).get(Ob.id_registration()) == 2:
            # првоеряем на регулярное выражение адрес почты
            if reg_ex.check_mail(message.text.strip()) == 1:
                # проверяем имеется ли такой адрес в БД otrs
                if DBProvide.get_count_mail(message.text.strip())[0][0] == 0:
                    DBProvideBot.b_update_table(id_client,Ob.id_registration(),3)
                    DBProvideBot.b_update_table(id_client,Ob.mail(),message.text.strip())
                    #user_all = DBProvideBot.b_get_all_user(id_client)
                    list_data = [DBProvideBot.b_get_all_user(id_client).get(Ob.mail()),
                                DBProvideBot.b_get_all_user(id_client).get(Ob.name_famyli()),
                                DBProvideBot.b_get_all_user(id_client).get(Ob.id_user())]
                    DBProvide.create_customer(list_data)
                    bot.send_message(id_client,"Регистрация прошла успешно!!!",parse_mode='Markdown')
                    start(message)
                else:
                    bot.send_message(message.from_user.id,f"Такой адрес имеется в системе, это ваш e-mail? {message.text.strip()}",
                                     reply_markup=menu_for_mail_update(message))
                    DBProvideBot.b_update_table(id_client,Ob.mail(),message.text)

            else:
                #print("Некорректный адрес")
                bot.send_message(message.from_user.id,
                                 "Не корректный адрес электронной почты, повторите ввод",parse_mode='Markdown')
        # 2- получаем Имя и Фамилию, и задаем вопрос о вводе маил
        if DBProvideBot.b_get_all_user(id_client).get(Ob.id_registration()) == 1:
            # получаем следующее сообщение считая его именем и фамилией
            if reg_ex.check_fio(message.text.strip()) == 1:
                DBProvideBot.b_update_table(id_client,Ob.name_famyli(),message.text.strip())
                DBProvideBot.b_update_table(id_client,Ob.id_registration(),2)
                bot.send_message(message.from_user.id,"Введите адрес электронной почты для обратной связи",parse_mode='Markdown')
            else:
                bot.send_message(message.from_user.id,"Некорректные данные, введите имя и фамилию через пробел",parse_mode='Markdown')
        # 1- задается первый вопрос при регистрации
        if DBProvideBot.b_get_all_user(id_client).get(Ob.id_registration()) == None:
            bot.send_message(message.from_user.id,"Введите Ваше имя и фамилию",parse_mode='Markdown')
            DBProvideBot.b_update_table(id_client,Ob.id_registration(),1)

# Формирование данных для создания новой заявки
def create_ticket(id_client,message):
    #print(DBProvideBot.b_get_all_user(id_client))
    list_data = [DBProvideBot.b_get_all_user(id_client).get(Ob.product_name()),
                    DBProvideBot.b_get_all_user(id_client).get(Ob.message_product())]

    if list_data[1] != None:
        out_data = DBProvide.full_request(list_data, id_client)
        file_name = DBProvideBot.b_get_file_name_on_user(id_client)
        if len(file_name) != 0:
            # скачиваем файлы
            download_file(file_name)
            i = 0
            while i < len(file_name):
                #encode_file.encode_file(file_name[i][0])
                DBProvide.create_article_attachment(encode_file.encode_file(f"{dirname}/{file_name[i][0]}"),out_data.get('id'),out_data.get('data_f'))
                #print(file_name[i][0])
                i += 1
            #print(file_name)
            if DBProvideBot.b_get_count_file(id_client)[0][0] > 5:
                bot.send_message(id_client,"Отправлено слишком много файлов, к заявке будут приложены только 5 файлов!",parse_mode='Markdown')
        bot.send_message(id_client,"Ваша заявка зарегистрирована, ответ поступит в течении 3-х рабочих дней",parse_mode='Markdown')
        delete_users(id_client)
    else:
        bot.send_message(id_client,"Вы не задали вопрос. Опишите проблему в текстовом поле!!!",parse_mode='Markdown')
    

def copy_text_on_file(id_client):
     # текст для обьединения с фотографией
    date_now = DT.datetime.now()
    dat = date_now.strftime('%H:%M:%S.%f')
    data_message = DBProvideBot.b_get_all_user(id_client).get(Ob.message_time)
    if len(DBProvideBot.b_get_file_time_max_and_text(id_client)) != 0:

        if DBProvideBot.b_get_all_user(id_client).get(Ob.message_product()) != None:
            if DBProvideBot.b_get_file_time_max_and_text(id_client)[0][0] < str(data_message):
                DBProvideBot.b_update_table(id_client,Ob.message_product(),
                    DBProvideBot.b_get_all_user(id_client).get(Ob.message_product()) +"\n"+
                    DBProvideBot.b_get_file_text(id_client,DBProvideBot.b_get_file_time_max_and_text(id_client)[0][0])[0][0])
            else:
  
                DBProvideBot.b_update_table(id_client,Ob.message_product(),
                    DBProvideBot.b_get_file_text(id_client,DBProvideBot.b_get_file_time_max_and_text(id_client)[0][0])[0][0]
                    +"\n"+ DBProvideBot.b_get_all_user(id_client).get(Ob.message_product()))
        else:
            DBProvideBot.b_update_table(id_client,Ob.message_product(),
                DBProvideBot.b_get_file_text(id_client,DBProvideBot.b_get_file_time_max_and_text(id_client)[0][0])[0][0])
    DBProvideBot.b_update_table(id_client,Ob.message_time(),str(dat))


# Функции для отрисовки меню
# кнопка для завршения работы в случае отказа от какого либо дейсвия
def menu_exit_client(message):  
     # стартовое меню.
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True,is_persistent=True)
    btn_ok = types.KeyboardButton("✅ Отправить")
    #btn_exit = types.KeyboardButton("Вернуться в начало")
    #btn_support = types.KeyboardButton("Обратиться в поддержку")
    markup1.add(btn_ok)
    #markup1.add(btn_exit,btn_support)
    return markup1
def menu_for_mail_update(message):
     # стартовое меню.
    markup_update = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_yes = types.KeyboardButton("Да")
    btn_exit = types.KeyboardButton("Нет")
    markup_update.add(btn_yes,btn_exit)
    return markup_update
def test_gg(message):      
    # создаем кнопки для выбора меню
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="✅ Отправить", callback_data='Input'))
    return markup
# кнопки для входа или регистрации
def menu_for_product(message):      
    # создаем кнопки для выбора меню
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=nabat, callback_data='Nabat'))
    markup.add(InlineKeyboardButton(text=arm_abi, callback_data='Armabi'))
    markup.add(InlineKeyboardButton(text=kp_sgp, callback_data='Sgp'))
    #  посылаем меню пользователю
    bot.send_message(message.from_user.id, "Выберите продукт", reply_markup = markup)

# отслеживание инлайн кнопок
#  отслеживание на какую кнопку нажали в инлайн кнопках
@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    req = call.data
    id_client = call.message.chat.id
    check_clik = 0
    # кнопки для определения по какому продукты задается вопрос
    if req == 'Nabat' and DBProvideBot.b_get_all_user(id_client).get(Ob.id_product()) == 2:
        check_clik = 1
        #print(call.text)
        bot.send_message(call.message.chat.id,f"Введите интересующий Вас вопрос по продукту {nabat}.\nДля регистрации запроса, "
        f"не забудьте нажать кнопку [Отправить]")
        DBProvideBot.b_update_table(id_client,Ob.product_name(),nabat)
        
    if req == 'Armabi' and DBProvideBot.b_get_all_user(id_client).get(Ob.id_product()) == 2:
        check_clik = 1
        bot.send_message(call.message.chat.id,f"Введите интересующий Вас вопрос по продукту {arm_abi}.\nДля регистрации запроса, "
        f"не забудьте нажать кнопку [Отправить]")
        DBProvideBot.b_update_table(id_client,Ob.product_name(),arm_abi)
        
    if req == 'Sgp' and DBProvideBot.b_get_all_user(id_client).get(Ob.id_product()) == 2:
        check_clik = 1
        bot.send_message(call.message.chat.id,f"Введите интересующий Вас вопрос по продукту {kp_sgp}.\nДля регистрации запроса, "
        f"не забудьте нажать кнопку [Отправить]")
        DBProvideBot.b_update_table(id_client,Ob.product_name(),kp_sgp)

    if req == 'Input' and DBProvideBot.b_get_all_user(id_client).get(Ob.id_product()) == 2:
        check_clik = 1
        if DBProvideBot.b_get_all_user(id_client).get(Ob.message_product()) != None or\
            len(DBProvideBot.b_get_file_name_on_user(id_client)) != 0:
            create_ticket(id_client,call.message)
    if check_clik == 0:
        bot.send_message(call.message.chat.id,"Для повторной подачи заявки напишите /start")
while True:
    try:
        bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
    except Exception as e:
        logger.file_log(f"Ошибка подключения к токен telegram bot {e}")
        #if count_connection_token != 3:
            
        #    count_connection_token += 1
        #else:
        #    logger.file_log("Большое количество попыток подключения к токен телеграма")
        #    raise SystemExit(1)
        time.sleep(60.0)
