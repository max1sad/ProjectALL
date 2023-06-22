import re
from  email_validate import validate, validate_or_fail
def check_fio(name):
    res = re.fullmatch(r'^[A-Za-zА-Яа-я]{2,20}\s[A-Za-zА-Яа-я]{2,20}$',name)
    if res:
        return 1
    else:
        return 0
def check_mail(mail):
        #resclient = re.fullmatch(r'^[\w\-\+=\.]*@[\w\-\+=\.]*$', mail)
        result = validate(email_address=mail,
                       check_format=True,
                       check_dns=False,
                       check_smtp=False,
                       check_blacklist=False)
        return result

#print(check_fio('Максимds Баранов'))
#print(check_mail('m.baranov@rusbitech.ru'))