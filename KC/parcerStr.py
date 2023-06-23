import os
def parcerStrFile(arr_file_all):
    i = 0
    result_mass = []
    # получаем данные с конфига, об объектах КЦ
    #arr_file_all = readFileConfControl("CONTROLSUM")
    while i < len(arr_file_all):
        result_mass.append(arr_file_all[i].split(';'))
        i += 1
    return result_mass

def checkFileOrCatalog(path_file):
    check = 0

    if os.path.isdir(str(path_file)):
        check =  1
    if os.path.isfile(str(path_file)):
        check = 2
    if check == 0:
        return 0
    else:
        return check
