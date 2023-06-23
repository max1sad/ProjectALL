import datetime as DT
import os
def logM(message):
    date_now = DT.datetime.now()
    dat = date_now.strftime('%Y-%m-%d %H:%M:%S')
    os.system("logger -t SKIF '{msg}'".format(msg=message))
    
