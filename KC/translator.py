# Переменная для указания языка перевода с русского на англ
# принимает два значения language = "en" и language = "ru" (Только для логирования событий в syslog)
language = "en"

path_lang = "/opt/Skif"
# чтение из файла
def read_file(path_file):
    with open(path_file) as f:
        resul = f.readlines()
    return resul

if language == "en":
    lang = read_file("{p}/lang/{l}".format(p=path_lang,l=language))

def tr(text):
    if language == "en":
        i = 0
        en_value = ''
        while i < len(lang):
            en = lang[i].split(":")
            if en[0].strip().lower() == text.strip().lower():
                en_value = en[1].strip()
                break
            i += 1
        if len(en_value) > 2:
            return en_value
        else:
            return text
    else:
        return text

#print(tr("Файл"))
#s = tr("Файл не найден")+" new{f}".format(f="gg")+"fg"
#print(s)