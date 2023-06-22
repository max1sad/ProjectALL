import datetime as DT
import os
def file_log(message):
    date_now = DT.datetime.now()
    dat = date_now.strftime('%Y-%m-%d %H:%M:%S')
    os.system(f"logger 'BOTTG: {message}'")
    #with open('/opt/BotTg/telegram_bot.log','a') as f:
    #    f.write(str(dat) + " " + message+ "\n")