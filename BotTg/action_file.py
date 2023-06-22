import os
import read_conf
import logger
dirname = os.path.dirname(__file__)
path_last_id = os.path.join(dirname, 'lastId')
def file_write(id_ticket):
    with open(path_last_id,'w') as f:
        f.write(id_ticket)
#file_write("12")

def file_read():
    if os.path.isfile(path_last_id):
        with open(path_last_id,'r') as f:
            return f.read()
    else:
        logger.file_log(f"файл {path_last_id} не найден!!!")