from PIL import Image
from ftplib import FTP

import config,subprocess, os, shutil

list_paths : list
path : str
name_file : str

def compressed_image(_img, _file_name):
    try:
        _img.save('compressed-' + _file_name, quality=50)
        os.remove(_file_name)
        os.rename('compressed-' + _file_name, _file_name)
    except Exception as e:
        os.remove(_file_name)
        report_error('Не удалось сжать: |' + _file_name + '| ' + str(e))

def get_name_file(_path):
    return _path.split('/')[-1]

def get_path(_path):
    _new_path : str = '/'
    _arr = _path.split('/')
    for i in range(2,len(_arr) - 1):
        _new_path += _arr[i] + '/'
    return _new_path

def get_list_paths():
    _list_paths = []
    with open ('list.txt', 'r') as f:
        _list_paths = f.read().split('\n')
    return _list_paths

def compress_png(input_file, output_file):
    try:
        subprocess.run(['pngquant', '--quality=65-80', '--output', output_file, input_file])
        os.remove(input_file)
        os.rename(output_file, input_file)
    except Exception as e:
        os.remove(input_file)
        report_error('Не удалось сжать: ' + input_file + ' ' + str(e))


def ftp_retrbinary(_ftp, _path, _name_file):
    global file_has

    try:
        _ftp.cwd('www' + _path)
    except Exception as e:
        report_error('Такого каталога нет: www' + _path)
        file_has = False
        _ftp.quit()
        return

    with open(_name_file, 'wb') as f:
        try:
            _ftp.retrbinary('RETR ' + _name_file, f.write)
        except Exception as e:
            file_has = False
            os.remove(_name_file)
            report_error('Такого файла нет: ' + _name_file)

def ftp_storbinary(_ftp, _path, _name_file):
    _ftp.cwd('www' + _path)
    _ftp.storbinary('STOR ' + _name_file, open(_name_file, 'rb'))

def file_format(_file_name):
    return _file_name.split('.')[-1]

def report_error(_error):
    array_error = []
    try:
        with open('error.txt', 'r') as f:
            array_error = f.read().split('\n')
    except FileNotFoundError:
        pass
    array_error.append(_error)
    with open('error.txt', 'w') as f:
        f.write('\n'.join(array_error))

def main():
    try:
        ftp = FTP(config.FTP)
        ftp.login(config.LOGIN, config.PASSWORD)
    except Exception as e:
        print('Не удалось подключиться к FTP: ' + str(e))
        return

    try:
        list_paths = get_list_paths()
    except Exception as e:
        print('Не удалось получить список путей: ' + str(e))
        ftp.quit()
        return

    file_has = True

    ftp_retrbinary(ftp, get_path('https://дымоход22.рф/upload/shop_1/1/5/2/item_1520/item_1327455.jpg'), get_name_file('https://дымоход22.рф/upload/shop_1/1/5/2/item_1520/item_1327455.jpg'))

    if file_has:
        if file_format(get_name_file('https://дымоход22.рф/upload/shop_1/1/5/2/item_1520/item_1327455.jpg')) == 'png':
            compress_png(get_name_file(list_paths[0]), 'compressed-' + get_name_file(list_paths[0]))
        else:
            compressed_image(Image.open(get_name_file('https://дымоход22.рф/upload/shop_1/1/5/2/item_1520/item_1327455.jpg')), get_name_file('https://дымоход22.рф/upload/shop_1/1/5/2/item_1520/item_1327455.jpg'))

    ftp.quit()


main()

# compressed_image(Image.open('item_image2056.png'))


# compress_png('item_image2056.png', 'compressed_item_image2056.png')



# ftp.cwd('www/дымоход22.рф/upload/shop_1/2/0/4/item_2043/')

# Получение списка файлов
# files = ftp.nlst()
# print(files)

# Загрузка файла
# with open('item_image2043.png', 'wb') as f:
#     ftp.retrbinary('RETR item_image2043.png', f.write)

# # Загрузка файла на сервер
# with open('local_file.txt', 'rb') as f:
#     ftp.storbinary('STOR remote_file.txt', f)

# Закрытие соединения
# ftp.quit()

