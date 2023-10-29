import numpy as np
import json
import os
import msgpack
import pickle
import csv

def main():
    task_1('tasks/matrix_53.npy')
    task_2('tasks/matrix_53_2.npy')
    task_3('tasks/products_53.json')
    task_4(path_file_product='tasks/products_53.json', path_file_price_info='tasks/price_info_53.json')
    task_5('answers/task_5/json_file.json')


def task_1(path_file: str):
    matrix = np.load(path_file)
    size = len(matrix)

    m_stat = dict()
    m_stat['sum'] = 0
    m_stat['avr'] = 0
    m_stat['sumMD'] = 0
    m_stat['avrMD'] = 0
    m_stat['sumSD'] = 0
    m_stat['avrSD'] = 0
    m_stat['max'] = matrix[0][0]
    m_stat['min'] = matrix[0][0]

    for i in range(0, size):
        for j in range(0, size):
            m_stat['sum'] += matrix[i][j]

            if i == j:
                m_stat['sumMD'] += matrix[i][j]

            if i + j == (size - 1):
                m_stat['sumSD'] += matrix[j][j]

            m_stat['max'] = max(m_stat['max'], matrix[i][j])
            m_stat['min'] = max(m_stat['min'], matrix[i][j])

    m_stat['avr'] = m_stat['sum'] / (size ** 2)
    m_stat['avrMD'] = m_stat['sumMD'] / size
    m_stat['avrSD'] = m_stat['sumSD'] / size

    for key in m_stat.keys():
        m_stat[key] = float(m_stat[key])

    with open('answers/matrix_stat.json', 'w') as file:
        file.write((json.dumps(m_stat)))

    norm_matrix = np.ndarray((size, size), dtype=float)

    for i in range(0, size):
        for j in range(0, size):
            norm_matrix[i][j] = matrix[i][j] / m_stat['sum']

    np.save('answers/norm_matrix', norm_matrix)


def task_2(path_file: str):
    matrix = np.load(path_file)
    size = len(matrix)

    x, y, z = list(), list(), list()

    limit = 500 + 53

    for i in range(0, size):
        for j in range(0, size):
            if matrix[i][j] > limit:
                x.append(i)
                y.append(j)
                z.append(matrix[i][j])

    np.savez('answers/points', x=x, y=y, z=z)
    np.savez_compressed('answers/points_zip', x=x, y=y, z=z)

    print(f'points     = {os.path.getsize("answers/points.npz")}')
    print(f'points_zip = {os.path.getsize("answers/points_zip.npz")}')


def task_3(path_file: str):
    with open(path_file) as file:
        data = json.load(file)

        products = dict()
        for item in data:
            if item['name'] in products:
                products[item['name']].append(item['price'])
            else:
                products[item['name']] = list()
                products[item['name']].append(item['price'])

        result = list()

        for name, prices in products.items():
            sum_price = 0
            max_price = prices[0]
            min_price = prices[0]
            size = len(prices)

            for price in prices:
                sum_price += price
                max_price = max(max_price, price)
                min_price = min(min_price, price)

            result.append({
                'name': name,
                'max': max_price,
                'min': min_price,
                'avr': sum_price / size,
            })

        # print(result)

        with open('answers/products_result.json', 'w') as r_json:
            r_json.write(json.dumps(result))

        with open('answers/products_result.msgpack', 'wb') as r_msgpack:
            r_msgpack.write(msgpack.dumps(result))

    print(f'products_result.json    = {os.path.getsize("answers/products_result.json")}')
    print(f'products_result.msgpack = {os.path.getsize("answers/products_result.msgpack")}')


def task_4(path_file_product: str, path_file_price_info: str):
    with open(path_file_product) as f:
        products = json.load(f)

    with open(path_file_price_info) as f:
        price_info = json.load(f)

    price_info_dict = dict()



    for item in price_info:
        price_info_dict[item['name']] = item

    for product in products:
        current_price_info = price_info_dict[product['name']]
        update_price(product, current_price_info)

    #print(products)

    with open("answers/products_updated.pkl", "wb") as f:
        f.write(pickle.dumps(products))


def update_price(product, price_info):
    method = price_info["method"]

    if method == "sum":
        product["price"] += price_info["param"]
    elif method == "sub":
        product["price"] -= price_info["param"]
    elif method == "percent+":
        product["price"] *= (1 + price_info["param"])
    elif method == "percent-":
        product["price"] *= (1 - price_info["param"])

    product["price"] = round(product["price"], 2)


def task_5(path_file: str):
    with open(path_file) as file:
        data = json.load(file)

    for i in data:
        print(i)

    keys = data[0].keys()

    with open("answers/task_5/csv_file.csv", 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

    with open("answers/task_5/pkl_file.pkl", "wb") as f:
        f.write(pickle.dumps(data))

    with open('answers/task_5/msgpack_file.msgpack', 'wb') as r_msgpack:
        r_msgpack.write(msgpack.dumps(data))

    print(f'json_file.json       = {os.path.getsize("answers/task_5/json_file.json")}')
    print(f'csv_file.csv         = {os.path.getsize("answers/task_5/csv_file.csv")}')
    print(f'pkl_file.pkl         = {os.path.getsize("answers/task_5/pkl_file.pkl")}')
    print(f'msgpack_file.msgpack = {os.path.getsize("answers/task_5/msgpack_file.msgpack")}')


if __name__ == '__main__':
    main()
