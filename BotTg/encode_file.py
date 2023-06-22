from pathlib import Path
import base64
import os
import logger
def encode_file(path_file):
    d = dict()
    # открываем файл, для кодирования в base64
    if os.path.isfile(path_file):
        with open(path_file, "rb") as image_file:
            encode_base64 = base64.b64encode(image_file.read())
        # получаем размер файла
        f = Path(path_file)
        sizi = f.stat().st_size
        # d.update(size_file_s)
        d.update(content=str(encode_base64)[2:len(encode_base64)+2])
        d.update(content_size=str(sizi))
        # в зависимости от длины пути, указываем какую часть имени выводить.
        #d.update(filename=path_file.split('/')[4])
        d.update(filename=os.path.basename(path_file))
        #print(d.get('name_file'))
        #print(d.values())
        os.remove(path_file)
    else:
        logger.file_log(f"Файл {path_file} не найден!!!")    
    return d
 
#print(os.path.basename("/tttt/tyt/gg.txt"))
#DBProvide.create_article_attachencode_file('./photos/file_3.jpg'),39,'2023-01-20 08:26:24')
