"""
Обрабатывает директорию с полученными zip архивами, разбирает вложенные xml файлы и формирует 2 csv файла:
Первый: id, level - по одной строке на каждый xml файл
Второй: id, object_name - по отдельной строке для каждого тэга object (получится от 1 до 10 строк на каждый xml файл)
"""
import os
import random
import string
import zipfile
import multiprocessing
import threading
from concurrent.futures import ThreadPoolExecutor, Executor, Future
import xml.etree.ElementTree as ET

lock_1 = threading.Lock()
lock_2 = threading.Lock()

file_name_1 = ''
file_name_2 = ''

def _processing(folder_name):
    for xml_file in xml_files:
        id  = get_id()
        level = get_level()
        object_names = get_objects_name()
        with lock_1:
            write(f"{id} {level}")
        with lock_2:
            for  object_name in  object_names:
                write(f"{id} {object_name }")


def processing():
    futures = []
    executor: Executor = ThreadPoolExecutor(max_workers=4)

    for archive in archives:
        folder = ....
        future = executor.submit(target=_processing, folder_name)
        futures.append(future)

    for f in futures:
        f.result(timeout=1)

    return

if __name__ == '__main__':
    processing()

