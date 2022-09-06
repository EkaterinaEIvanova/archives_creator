"""
Обрабатывает директорию с полученными zip архивами, разбирает вложенные xml файлы и формирует 2 csv файла:
Первый: id, level - по одной строке на каждый xml файл
Второй: id, object_name - по отдельной строке для каждого тэга object (получится от 1 до 10 строк на каждый xml файл)
"""
import os
import csv
import timeit
import zipfile
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, Executor, Future, ProcessPoolExecutor
from typing import List

from lxml import etree


lock_1 = multiprocessing.Lock()
lock_2 = multiprocessing.Lock()
# lock_1 = threading.Lock()
# lock_2 = threading.Lock()


def _processing(archive_name):
    with zipfile.ZipFile(archive_name) as myzip:
        for n in range(1, 101):
            with myzip.open(f"test_{n}.xml", mode='r') as xml_file:
                tree = etree.parse(xml_file)
                var_id = tree.xpath('./var[@name="id"]/text()')[0]
                level = tree.xpath('./var[@name="level"]/text()')[0]
                nodes = ((var_id, node.get('name')) for node in tree.iterfind('./objects/object'))

            with lock_1:
                with open('csv_file_1', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow((var_id, level))

            with lock_2:
                with open('csv_file_2', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(nodes)


def processing():
    futures: List[Future] = []
    # executor: Executor = ProcessPoolExecutor(max_workers=4)
    executor: Executor = ThreadPoolExecutor(max_workers=4)

    for archive_name in os.listdir("archives"):
        full_archive_name = f"archives/{archive_name}"
        if zipfile.is_zipfile(full_archive_name):
            future = executor.submit(_processing, full_archive_name)
            futures.append(future)

    for f in futures:
        f.result(timeout=1)


if __name__ == '__main__':
    start = timeit.default_timer()
    for file_name in ('csv_file_1', 'csv_file_2'):
        with open(file_name, 'w', newline='') as f:
            pass
    processing()
    stop = timeit.default_timer()
    execution_time = stop - start
    print(execution_time)  # It returns time in sec

