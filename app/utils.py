import math
import numpy as np
import csv
import os
from app import app, db
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from app.models import Task
from time import sleep


def randomize(rMin, rMax, fiMin, fiMax, gMin, gMax):
    rObj = np.random.uniform(rMin, rMax)
    fiObj = np.random.uniform(fiMin, fiMax)
    gObj = np.random.uniform(gMin, gMax)
    xObj = rObj * math.cos(fiObj)
    yObj = rObj * math.sin(fiObj)
    return xObj, yObj, gObj, fiObj, rObj


def randomize_test_case(x_start, x_end, y_start, y_end, i, n):
    x_delta = (x_end - x_start) / n
    y_delta = (y_end - y_start) / n
    xObj = x_start + x_delta * i + 0.01
    yObj = y_start + y_delta * i + 0.01
    rObj = math.sqrt(pow(xObj, 2) + pow(yObj, 2))
    fiObj = math.atan(yObj / abs(xObj))
    if xObj < 0:
        fiObj = math.pi - fiObj
    gObj = 4
    return xObj, yObj, gObj, fiObj, rObj


def valid(xObj, yObj, gObj, h, l):
    t = math.sqrt(4 * pow(h, 2) - pow(l, 2)) * yObj
    cond1 = t + l * xObj > l * h
    cond2 = t - l * xObj > l * h
    cond3 = abs(-l * xObj - t + l * h) > 2 * h * gObj
    cond4 = abs(l * xObj - t + l * h) > 2 * h * gObj
    return cond1 and cond2 and cond3 and cond4


def F_a(x, y, r, h):
    if y >= 0 and x + h >= 0:
        return math.asin(y / r)
    elif y >= 0 and x + h < 0:
        return math.pi - math.asin(y / r)
    elif y < 0 and x + h < 0:
        return math.pi + math.asin(abs(y) / r)
    elif y < 0 and x + h >= 0:
        return 2 * math.pi - math.asin(abs(y) / r)


def F_b(x, y, r, h):
    if y >= 0 and x - h >= 0:
        return math.asin(y / r)
    elif y >= 0 and x - h < 0:
        return math.pi - math.asin(y / r)
    elif y < 0 and x - h < 0:
        return math.pi + math.asin(abs(y) / r)
    elif y < 0 and x - h >= 0:
        return 2 * math.pi - math.asin(abs(y) / r)


def count(xObj, yObj, h, gObj, m):
    rA = math.sqrt(pow((xObj + h), 2) + pow(yObj, 2))
    fiA = F_a(xObj, yObj, rA, h)
    rB = math.sqrt(pow((xObj - h), 2) + pow(yObj, 2))
    fiB = F_b(xObj, yObj, rB, h)
    L_a = math.floor((m / (2 * math.pi)) * (fiA - math.asin(gObj / rA)))
    R_a = math.floor((m / (2 * math.pi)) * (fiA + math.asin(gObj / rA)))
    L_b = math.floor((m / (2 * math.pi)) * (fiB - math.asin(gObj / rB)))
    R_b = math.floor((m / (2 * math.pi)) * (fiB + math.asin(gObj / rB)))
    return L_a, R_a, L_b, R_b


def generate_usual_way(h, l, m, n, rMin, rMax, fiMin, fiMax, gMin, gMax, task_id):
    M = []
    precedents = 0
    while precedents < n:
        beta_A = [0] * m
        beta_B = [0] * m
        flag = False
        while not flag:
            xObj, yObj, gObj, fiObj, rObj = randomize(rMin, rMax, fiMin, fiMax, gMin, gMax)
            if not valid(xObj, yObj, gObj, h, l):
                continue
            L_a, R_a, L_b, R_b = count(xObj, yObj, h, gObj, m)
            flag = L_a != R_a
        precedents += 1
        Task.query.get(task_id).produced += 1
        db.session.commit()
        for j in range(L_a, R_a + 1):
            beta_A[j] = 1
        for j in range(L_b, R_b + 1):
            beta_B[j] = 1
        M.append({'beta_A': beta_A, 'beta_B': beta_B, 'rObj': rObj, 'fiObj': fiObj,
                  'gObj': gObj, 'xObj': xObj, 'yObj': yObj, 'h': h, 'l': l})
    save_to_file_special(dataset_name=f'dataset_{task_id}',
                         dataset_folder='', dataset=M, h=h, l=l,
                         m=m, g_min=gMin, g_max=gMax, fi_min=fiMin, fi_max=fiMax, r_min=rMin,
                         r_max=rMax, n=n)
    #save_to_file(M, task_id)


def generate_test_case(h, l, m, n, x_start, x_end, y_start, y_end, task_id):
    M = []
    if x_start> x_end:
        x_start, x_end = x_end, x_start
    precedents = 0
    while precedents < n:
        beta_A = [0] * m
        beta_B = [0] * m
        flag = False
        flag2 = False
        while not flag:
            xObj, yObj, gObj, fiObj, rObj = randomize_test_case(x_start, x_end, y_start, y_end, precedents, n)
            if not valid(xObj, yObj, gObj, h, l):
                flag2 = True
                flag = True
            else:
                L_a, R_a, L_b, R_b = count(xObj, yObj, h, gObj, m)
                flag = L_a != R_a
            if not flag2 and not flag:
                flag2 = True
                break
        precedents += 1
        Task.query.get(task_id).produced += 1
        db.session.commit()
        if flag2:
            continue
        for j in range(L_a, R_a + 1):
            beta_A[j] = 1
        for j in range(L_b, R_b + 1):
            beta_B[j] = 1
        M.append({'beta_A': beta_A, 'beta_B': beta_B, 'rObj': rObj, 'fiObj': fiObj,
                  'gObj': gObj, 'xObj': xObj, 'yObj': yObj, 'h': h, 'l': l})
    save_to_file(M, task_id)


def save_to_file(dataset, task_id):
    filename = os.path.join(app.root_path, 'datasets', f'dataset_{task_id}.csv')
    with open(filename, 'w', newline='') as output:
        writer = csv.writer(output, delimiter=';')
        for row in dataset:
            inserting_row = row['beta_A'] + row['beta_B'] + [row['rObj'], row['fiObj'], row['gObj'], row['xObj'],
                                                             row['yObj'], row['h'], row['l']]
            writer.writerow(inserting_row)


def get_dataset(m, h, l, n, rMin, rMax, fiMin, fiMax, gMin, gMax, task_id):
    M = []
    precedents = 0
    while precedents < n:
        beta_A = [0] * m
        beta_B = [0] * m
        flag = False
        while not flag:
            xObj, yObj, gObj, fiObj, rObj = randomize(rMin, rMax, fiMin, fiMax, gMin, gMax)
            if not valid(xObj, yObj, gObj, h, l):
                continue
            L_a, R_a, L_b, R_b = count(xObj, yObj, h, gObj, m)
            flag = L_a != R_a
        precedents += 1
        Task.query.get(task_id).produced += 1
        db.session.commit()
        for j in range(L_a, R_a + 1):
            beta_A[j] = 1
        for j in range(L_b, R_b + 1):
            beta_B[j] = 1
        M.append({'beta_A': beta_A, 'beta_B': beta_B, 'rObj': rObj, 'fiObj': fiObj,
                  'gObj': gObj, 'xObj': xObj, 'yObj': yObj})
    return M


def generate_const_g_diff_m(h, l, n, rMin, rMax, fiMin, fiMax, item_list, tasks):
    for task in tasks:
        for g in item_list:
            M = get_dataset(m=task['diff_item'], h=h, l=l, n=n, rMin=rMin, rMax=rMax, fiMin=fiMin, fiMax=fiMax, gMin=g,
                            gMax=g, task_id=task['id'])
            save_to_file_special(dataset_name=f'g_const_{g}_m_diff_{task["diff_item"]}',
                                 dataset_folder='g_const_m_diff', dataset=M, h=h, l=l,
                                 m=task['diff_item'], g_min=g, g_max=g, fi_min=fiMin, fi_max=fiMax, r_min=rMin,
                                 r_max=rMax, n=n)


def generate_const_g_diff_h(m, l, n, rMin, rMax, fiMin, fiMax, item_list, tasks):
    for task in tasks:
        for g in item_list:
            M = get_dataset(m=m, h=task['diff_item'], l=l, n=n, rMin=rMin, rMax=rMax, fiMin=fiMin, fiMax=fiMax, gMin=g,
                            gMax=g, task_id=task['id'])
            save_to_file_special(dataset_name=f'g_const_{g}_h_diff_{task["diff_item"]}',
                                 dataset_folder='g_const_h_diff', dataset=M, h=task['diff_item'], l=l,
                                 m=m, g_min=g, g_max=g, fi_min=fiMin, fi_max=fiMax, r_min=rMin, r_max=rMax, n=n)


def generate_const_g_diff_l(m, h, n, rMin, rMax, fiMin, fiMax, item_list, tasks):
    for task in tasks:
        for g in item_list:
            M = get_dataset(m=m, h=h, l=task['diff_item'], n=n, rMin=rMin, rMax=rMax, fiMin=fiMin, fiMax=fiMax, gMin=g,
                            gMax=g, task_id=task['id'])
            save_to_file_special(dataset_name=f'g_const_{g}_l_diff_{task["diff_item"]}',
                                 dataset_folder='g_const_l_diff', dataset=M, h=h, l=task['diff_item'],
                                 m=m, g_min=g, g_max=g, fi_min=fiMin, fi_max=fiMax, r_min=rMin, r_max=rMax, n=n)


def generate_const_g_diff_r(m, l, n, rMin, h, fiMin, fiMax, item_list, tasks):
    for task in tasks:
        for g in item_list:
            M = get_dataset(m=m, h=h, l=l, n=n, rMin=rMin, rMax=task['diff_item'], fiMin=fiMin, fiMax=fiMax, gMin=g,
                            gMax=g, task_id=task['id'])
            save_to_file_special(dataset_name=f'g_const_{g}_r_diff_{task["diff_item"]}',
                                 dataset_folder='g_const_r_diff', dataset=M, h=h, l=l, m=m,
                                 g_min=g, g_max=g, fi_min=fiMin, fi_max=fiMax, r_min=rMin, r_max=task['diff_item'], n=n)


def save_to_file_special(dataset_name, dataset_folder, dataset, h, l, m, g_min, g_max, fi_min, fi_max, r_min, r_max, n):
    path = os.path.join(app.root_path, 'datasets', dataset_folder)
    if not os.path.exists(path):
        os.makedirs(path)
    if not '.csv' in dataset_name:
        dataset_name = dataset_name + '.csv'
    filename = os.path.join(path, dataset_name)
    with open(filename, 'w', newline='') as output:
        writer = csv.writer(output, delimiter=';')
        meta_row = [h, l, m, g_min, g_max, fi_min, fi_max, r_min, r_max, n]
        writer.writerow(meta_row)
        for row in dataset:
            inserting_row = row['beta_A'] + row['beta_B'] + [row['rObj'], row['fiObj'], row['gObj'], row['xObj'],
                                                             row['yObj']]
            writer.writerow(inserting_row)


def save_files(uploaded_files):
    counter = len([name for name in os.listdir(os.path.join(app.root_path, 'uploads')) if not os.path.isfile(name)])
    path = os.path.join(app.root_path, 'uploads', str(counter + 1))
    os.makedirs(path)
    for file in uploaded_files:
        filename = file.filename
        if len(file.filename.split('/')) > 1:
            filename = file.filename.split('/')[-1]
        if len(file.filename.split('\\')) > 1:
            filename = file.filename.split('\\')[-1]
        file.save(os.path.join(path, f'{filename}.csv'))
    return path


def count_repeats(dataset_path, m):
    repeats = {}
    with open(dataset_path) as file:
        reader = csv.reader(file, delimiter=';')
        meta_info = next(reader)
        m = int(meta_info[2])
        for row in reader:
            mask = tuple(row[:2 * m])
            if mask in repeats:
                repeats[mask] += 1
            else:
                repeats[mask] = 1
    return sum(repeats[mask] for mask in repeats) - len(repeats), meta_info


def make_plot(uploaded_files, const_item_name, diff_item_name, xlabel_legend, ylabel_legend):
    filepath = save_files(uploaded_files)
    results = {}
    meta_info = []
    for file in os.listdir(filepath):
        components = file[:-4].split('_')
        const_item = int(components[2])
        diff_item = int(components[-1].split('.')[0])
        repeats, meta_info = count_repeats(os.path.join(filepath, file), diff_item)
        if const_item in results:
            results[const_item][diff_item_name].append(diff_item)
            results[const_item]['repeats'].append(repeats)
        else:
            results[const_item] = {diff_item_name: [diff_item], 'repeats': [repeats]}
    fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
    for const_item in results:
        diff_items = results[const_item][diff_item_name]
        repeats = results[const_item]['repeats']
        x = zip(diff_items, repeats)
        xs = sorted(x, key=lambda tup: tup[0])
        diff_items = [x[0] for x in xs]
        repeats = [x[1] for x in xs]
        ax.plot(diff_items, repeats, linewidth=3, label=f'{const_item_name} = {const_item}', marker='o')
    ax.grid()
    plt.xlabel(xlabel_legend)
    plt.ylabel(ylabel_legend)
    plt.legend()
    counter = len([name for name in os.listdir(os.path.join(app.root_path, 'static', 'analysis_images'))])
    im_path = os.path.join(app.root_path, 'static', 'analysis_images', f'{counter + 1}.png')
    plt.savefig(im_path)
    plt.clf()
    plt.close()
    return f'{counter + 1}.png', meta_info


def clean_dataset(uploaded_file):
    filepath = save_files([uploaded_file])
    repeats = {}
    clear_dataset = []
    for file in os.listdir(filepath):
        with open(os.path.join(filepath, file)) as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            meta_info = next(reader)
            clear_dataset.append(meta_info)
            m = int(meta_info[2])
            for row in reader:
                mask = tuple(row[:2 * m])
                if mask in repeats:
                    repeats[mask] += 1
                else:
                    repeats[mask] = 1
                    clear_dataset.append(row)

    counter = len([name for name in os.listdir(os.path.join(app.root_path, 'datasets')) if os.path.isfile(name)])
    path = os.path.join(app.root_path, 'datasets', f'clear_dataset_{str(counter + 1)}.csv')
    with open(path, 'w') as file:
        writer = csv.writer(file, delimiter=';')
        for row in clear_dataset:
            writer.writerow(row)
    dataset_name = f'clear_dataset_{str(counter + 1)}.csv'
    return dataset_name
