import math
import numpy as np
import csv
import os
from app import app, db
from flask import flash
from app.models import Task


def randomize(rMin, rMax, fiMin, fiMax, gMin, gMax, i, h):
    rObj = np.random.uniform(rMin, rMax)
    fiObj = np.random.uniform(fiMin, fiMax)
    gObj = np.random.uniform(gMin, gMax)
    xObj = rObj * math.cos(fiObj)
    yObj = rObj * math.sin(fiObj)
    # Генерация для диагонального движения с углом 45 градусов

    # xObj = -550 + i + 0.01
    # yObj = rMax - i
    # rObj = math.sqrt(pow(xObj, 2) + pow(yObj, 2))
    # # if xObj < 0:
    # #     fiObj = math.atan(abs(xObj) / yObj) + math.pi / 2
    # # else:
    # #     fiObj = math.atan(xObj / yObj)
    # fiObj = math.atan(yObj / abs(xObj))
    # if xObj < 0:
    #     fiObj = math.pi - fiObj
    # gObj = 4
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


def generate(h, l, m, n, rMin, rMax, fiMin, fiMax, gMin, gMax, lambd, gamma, task_id, add):
    M = []
    precedents = 0
    while precedents < n:
        beta_A = [0] * m
        beta_B = [0] * m
        flag = False
        flag2 = False  # для нового генератора
        while not flag:
            xObj, yObj, gObj, fiObj, rObj = randomize(rMin, rMax, fiMin, fiMax, gMin, gMax, precedents, h)
            if not valid(xObj, yObj, gObj, h, l):
                #flag2 = True
                continue
            #if not flag2:
            L_a, R_a, L_b, R_b = count(xObj, yObj, h, gObj, m)
            flag = L_a != R_a
            # flag = True
            # if flag2:
            #     flag = True
            # else:
            #     flag = L_a != R_a
        precedents += 1
        #print(precedents)
        Task.query.get(task_id).produced += 1
        db.session.commit()
        # if flag2:
        #     continue

        # if rObj < rMin:
        #     Task.query.get(task_id).produced = n
        #     db.session.commit()
        #     precedents = n
        for j in range(L_a, R_a + 1):
            beta_A[j] = 1
        for j in range(L_b, R_b + 1):
            beta_B[j] = 1
        d = 0.1
        #d = math.tanh(lambd * (rObj / h))
        a = 0.2
        #a = 1 / (1 + math.exp(-gamma * (math.pi / 2 - fiObj)))
        r = (h / lambd) * math.atanh(d)
        fi = math.pi / 2 + (1 / gamma) * math.log((1-a) / a)
        M.append({'beta_A': beta_A, 'beta_B': beta_B, 'd': d, 'a': a, 'r': r, 'fi': fi, 'rObj': rObj, 'fiObj': fiObj,
                  'gObj': gObj, 'xObj': xObj, 'yObj': yObj, 'h': h, 'l': l})
    save_to_file(M, m, add, task_id)


def save_to_file(dataset, m, add, task_id):
    print("SAVED")
    # if add:
    #     filename = os.path.join(app.root_path, 'datasets', f'dataset-full-{m}.csv')
    # else:
    #     filename = os.path.join(app.root_path, 'datasets', f'dataset-{m}.csv')
    filename = os.path.join(app.root_path, 'datasets', f'dataset_{task_id}.csv')
    #filename = f'dataset-handmade-diagonal-enhance-{m}.csv'
    with open(filename, 'w', newline='') as output:
        writer = csv.writer(output, delimiter=';')
        for row in dataset:
            inserting_row = row['beta_A'] + row['beta_B'] + [row['rObj'], row['fiObj']]
            if add:
                #inserting_row += [row['r'], row['fi']]
                inserting_row += [row['r'], row['fi'], row['rObj'], row['fiObj'], row['gObj'], row['xObj'], row['yObj'], row['h'], row['l']]
            writer.writerow(inserting_row)
