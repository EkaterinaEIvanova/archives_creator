"""
1. Создает 50 zip-архивов, в каждом 100 xml файлов со случайными данными следующей структуры:

<root>
<var name=’id’ value=’<случайное уникальное строковое значение>’/>
<var name=’level’ value=’<случайное число от 1 до 100>’/>
<objects><object name=’<случайное строковое значение>’/>
<object name=’<случайное строковое значение>’/>
…
</objects>
</root>

В тэге objects случайное число (от 1 до 10) вложенных тэгов object.
"""
import os
import random
import string
import zipfile

import xml.etree.ElementTree as ET


def create_xml_file():
    root = ET.Element('root')

    id = ET.Element('var', name="id")
    id.text = ''.join(random.choices(string.ascii_lowercase, k=5))
    root.append(id)

    level = ET.Element('var', name="level")
    level.text = str(random.randint(1, 100))
    root.append(level)

    objects = ET.Element('objects')

    for i in range(0, random.randint(1, 10)):
        name = ''.join(random.choices(string.ascii_lowercase, k=10))
        objects.append(ET.Element('object', name=name))

    root.append(objects)
    indent(root)

    return root


def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def create_xml_files():
    for n in range(1, 101):
        ET.ElementTree(create_xml_file()).write(f"test_{n}.xml")


def create_folder(name: str):
    if not os.path.isdir(name):
        os.mkdir(name)
    os.chdir(name)


def create_archive(n: int):
    with zipfile.ZipFile(f"archive_{n}.zip", 'w', zipfile.ZIP_DEFLATED, True) as myzip:
        for root, dirs, files in os.walk(f"folder_{n}"):
            for file in files:
                myzip.write(os.path.join(root, file), arcname=os.path.join('', file))


def create_archives():
    create_folder("archives")

    for i in range(1, 51):
        create_folder(f"folder_{i}")
        create_xml_files()
        os.chdir("..")
        create_archive(i)
        # os.remove(f"folder_{i}")


if __name__ == '__main__':
    create_archives()

