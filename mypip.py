import os
import requests
from lxml import html
import re
import tarfile
import urllib.request
import zipfile
import graphviz
from io import BytesIO
from urllib.request import urlopen




#get link of package
def get_link(package_name):
    url = "https://pypi.org/simple/" + package_name
    try:
        response = requests.get(url)
    except(Exception):
        return 'ConnectionError or no such package'
    if (response.status_code == 200):
        body = html.fromstring(response.text)
        massiv = body.xpath('//a/@href')
        #print(massiv)
        if(len(massiv)!=0):
            return massiv[-1]
        return 'There are no versions of this package'

    return 'No such package'

def get_children(file_name):
    children = []

    for dirpath, dirnames, filenames in os.walk('c:\\temp\\' + file_name):
        # перебрать файлы
        for filename in filenames:

            if (filename == 'requires.txt'):
                with open(os.path.join(dirpath, filename), 'r') as file3:

                    lines = file3.readlines()
                    regex = re.compile('^[a-z0-9_\.-]*')

                    for line in lines:
                        s = regex.match(line)
                        if(s.group()!=''):
                            children.append(s.group())

            elif(filename.startswith("METADATA")):
                with open(os.path.join(dirpath, filename), 'r') as file3:
                    lines = file3.readlines()
                    #regex = re.compile('^[a-z0-9_\.-]*')
                    for line in lines:
                        if(line.startswith('Requires-Dist')):
                            temp = line.split()
                            children.append(temp[1])

    return children

def do_child(children, pack):
    for child in children:
        dot.edge(pack,child)
        print(child)
        if(child not in allnames):
            allnames.add(child)
            print_package(child)


def print_package(package):
    children = []

    url = get_link(package)
    allnames.add(package)
    if (url != 'There are no versions of this package' and url!='ConnectionError or no such package' and url!='No such package'):
        urls = url.split('/')
        file_name = urls[-1].split('#')[0]
        try:
            urllib.request.urlretrieve(url, file_name)
        except(Exception):
                print('Exeption occured')
                return

        if (('tar.gz' in file_name) or ('tar.bz2' in file_name)):
            tar = tarfile.open(file_name, 'r')
            tar.extractall('c:\\temp')
            children = get_children(file_name.split('.tar')[0])
            do_child(children, package)

        else:
            with open('c:\\temp\\' + package + '.zip', "wb") as file:
                with open(file_name, 'rb') as file2:
                    file.write(file2.read())
            z = zipfile.ZipFile('c:\\temp\\' + package + '.zip', 'r')
            z.extractall('c:\\temp\\' + package)
            z.close()
            children = get_children(package)
            do_child(children, package)

    elif(url=='There are no versions of this package'):
        print('There are no versions of this package')
    else:
        print('ConnectionError or no such package')


if __name__ == '__main__':
    package_name = input('Enter package name: ')
    allnames = set()
    names = []
    dot = graphviz.Digraph()
    print_package(package_name)
    dot.name = package_name
    print(dot.source)

