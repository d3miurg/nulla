import sys
import os
import platform

def start():
    platform_info = platform.platform()
    if 'Windows' in platform_info:
        status = os.system('python -m pip install amino.fix')
        if status != 0:
            print('Выход (невозможно использовать pip)')
            sys.exit()

    elif 'Linux' in platform_info:
        print('Установка пакетов на Linux-платформах может потребовать рут-права')
        
        if 'debian' in platform_info:
            status = os.system('pip3 install amino.fix')

            if status != 0:
                print('Невозможно использовать pip. Установка')
                sub_status = os.system('sudo apt install python3-pip')

                if sub_status != 0:
                    print('Выход (невозможно установить pip)')
                    sys.exit()

        else:
            status = os.system('pip3 install amino.fix')

            if status != 0:
                print('Невозможно использовать pip. Установка')
                sub_status = os.system('pkg install python3-pip')

                if sub_status != 0:
                    print('Выход (невозможно установить pip)')
                    sys.exit()
    
    for directory in sys.path:
        if 'site-packages' in directory:
            file = open(directory + '/websocket/_app.py', 'r')
            data = file.read()
            file.close()
            data = data.replace('isAlive', 'is_alive')
            file = open(directory + '/websocket/_app.py', 'w')
            file.write(data)
            file.close()

    cont = input()
