import os
import subprocess

'''
1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
и также проверить тип и содержимое переменных.
'''

str1 = 'разработка'
str2 = 'сокет'
str3 = 'декоратор'
print(type(str1))
print(str1)
print(type(str2))
print(str2)
print(type(str3))
print(str3)
print('\t')

'''
2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов 
(не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
'''

str4 = b'class'
str5 = b'function'
str6 = b'method'
print(type(str4))
print(str4)
print(len(str4))
print(type(str5))
print(str5)
print(len(str5))
print(type(str6))
print(str6)
print(len(str6))
print('\t')

'''
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
'''

str7 = b'attribute'
print(str7)
# str8 = b'класс'
# print(str8)
# str9 = b'функция'
# print(str9)
str10 = b'type'
print(str10)
print('\t')

'''
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое 
и выполнить обратное преобразование (используя методы encode и decode).
'''

str11 = 'разработка'
str12 = 'администрирование'
str13 = 'protocol'
str14 = 'standard'
str11_bytes = str11.encode('utf-8')
str12_bytes = str.encode(str12, encoding='utf-8')
str13_bytes = str13.encode('utf-8')
str14_bytes = str.encode(str14, encoding='utf-8')
print(str11_bytes)
print(type(str11_bytes))
print(str12_bytes)
print(type(str12_bytes))
print(str13_bytes)
print(type(str13_bytes))
print(str14_bytes)
print(type(str14_bytes))
print('\t')
str11_str = str11_bytes.decode('utf-8')
str12_str = bytes.decode(str12_bytes, encoding='utf-8')
str13_str = str13_bytes.decode('utf-8')
str14_str = bytes.decode(str14_bytes, encoding='utf-8')
print(str11_str)
print(type(str11_str))
print(str12_str)
print(type(str12_str))
print(str13_str)
print(type(str13_str))
print(str14_str)
print(type(str14_str))
print('\t')

'''
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип 
на кириллице.
'''

args1 = ['ping', 'yandex.ru']
args2 = ['ping', 'youtube.com']
spr_ping1 = subprocess.Popen(args1, stdout=subprocess.PIPE)
spr_ping2 = subprocess.Popen(args2, stdout=subprocess.PIPE)

for _ in spr_ping1.stdout:
    # print(_)
    _ = _.decode('cp866').encode('utf-8')
    print(_.decode('utf-8'))

for _ in spr_ping2.stdout:
    # print(_)
    _ = _.decode('cp866').encode('utf-8')
    print(_.decode('utf-8'))

'''
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
'''

DIR = 'data'

with open(os.path.join(DIR, 'test_file.txt'), 'w', encoding='UTF-8') as f_w:
    f_w.write('сетевое программирование\n')
    f_w.write('сокет\n')
    f_w.write('декоратор')
    f_w.close()

with open(os.path.join(DIR, 'test_file.txt'), 'r') as f_r1:
    for _ in f_r1:
        print(_)
print('\t')
with open(os.path.join(DIR, 'test_file.txt'), 'r', encoding='UTF-8') as f_r2:
    for _ in f_r2:
        print(_)
