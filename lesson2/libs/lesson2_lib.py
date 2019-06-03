# библиотека функций

import os
import re
import csv


def get_data(d, f_list):
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    p1 = 'Изготовитель системы'
    p2 = 'Название ОС'
    p3 = 'Код продукта'
    p4 = 'Тип системы'
    headers = [p1, p2, p3, p4]
    for f in f_list:
        with open(os.path.join(d, f)) as f_r:
            for _ in f_r:
                if re.match(p1, _):
                    l1 = re.findall(r'\s([A-Z]+)\n', _)
                    for l in l1:
                        os_prod_list.append(l)
                elif re.match(p2, _):
                    l2 = re.findall(r'\s{22}([A-Za-zА-Яа-я0-9. ]+)\n', _)
                    for l in l2:
                        os_name_list.append(l)
                elif re.match(p3, _):
                    l3 = re.findall(r'\s([A-Z0-9-]+)\n', _)
                    for l in l3:
                        os_code_list.append(l)
                elif re.match(p4, _):
                    l4 = re.findall(r'\s{22}([A-Za-z0-9- ]+)\n', _)
                    for l in l4:
                        os_type_list.append(l)
    main_data = [headers]
    for i in range(3):
        t = []
        t = [os_prod_list[i],os_name_list[i],os_code_list[i],os_type_list[i]]
        main_data.append(t)
    return main_data


def write_to_csv(d, f_name, l_name):
    with open(os.path.join(d, f_name), 'w', encoding='UTF-8') as f_w:
        writer = csv.writer(f_w, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(l_name)
    return


