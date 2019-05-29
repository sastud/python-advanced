
str1 = 'разработка'
str2 = 'socket'
str3 = 'декоратор'

'''
1. Реализовать приведение строк "разработка", "сокет", "декоратор" к типу bytes используя нативные методы строк;
'''

str1_bytes = str1.encode('utf-8')
str2_bytes = str2.encode('utf-8')
str3_bytes = str.encode(str3, encoding='utf-8')
print(str1_bytes)
print(type(str1_bytes))
print(str2_bytes)
print(type(str2_bytes))
print(str3_bytes)
print(type(str3_bytes))
print('\t')

'''
2. Реализовать приведение полученных экземпляров типа bytes к типу str
'''

str1_str = str1_bytes.decode('utf-8')
str2_str = str2_bytes.decode('utf-8')
str3_str = bytes.decode(str3_bytes, encoding='utf-8')
print(str1_str)
print(type(str1_str))
print(str2_str)
print(type(str2_str))
print(str3_str)
print(type(str3_str))
print('\t')

'''
3. Реализовать приведение полученных строк и байтовых последовательностей с использованием различных кодировок utf-8 
latin-1
'''

print(str1_bytes.decode('latin-1'))
print(str2_bytes.decode('latin-1'))
print(str3_bytes.decode('latin-1'))

# str1_bytes_lat1 = str1.encode('latin-1')
# print(str1_bytes_lat1)
# print(str1_bytes_lat1.decode('utf-8'))

str2_bytes_lat1 = str2.encode('latin-1')
print(str2_bytes_lat1)
print(str2_bytes_lat1.decode('utf-8'))

# str3_bytes_lat1 = str3.encode('latin-1')
# print(str3_bytes_lat1)
# print(str3_bytes_lat1.decode('utf-8'))
