import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Visualizer:
    def __init__(self, ommatidia_number, file_path):
        self._ommatidia_number = ommatidia_number
        self._file_path = file_path
        with open(file_path) as file:
            self._rows = file.readlines()
        self._rows = [row.split(';') for row in self._rows]
        fig1 = plt.figure()
        self._axes = fig1.add_subplot(111, aspect='equal')
        self._up = 0
        self._bottom = -0
        self._left = -0
        self._right = 0

    def _update_borders(self, left, right, up, bottom):
        if left < self._left:
            self._left = left
        if right > self._right:
            self._right = right
        if bottom < self._bottom:
            self._bottom = bottom
        if up > self._up:
            self._up = up

    def _visualize_eyes(self, h, l):
        #self._axes.add_patch(plt.Circle((-h, 0), 1, color='black'))
        #self._axes.add_patch(plt.Circle((h, 0), 1, color='black'))
        self._axes.add_patch(plt.Circle((h, 0), l, color='black', fill=False))
        self._axes.add_patch(plt.Circle((-h, 0), l, color='black', fill=False))

    def _visualize_object(self, xObj, yObj, gObj, color, fill=True):
        self._axes.add_patch(plt.Circle((xObj, yObj), gObj, color=color, fill=fill))

    def visualize_all(self, step):
        for i in range(0, len(self._rows), step):
            if i == 0:
                self.visualize_precedent(i, False, True, False)
            else:
                self.visualize_precedent(i, False, False, False)
        self.show()

    def visualize_precedent(self, index, show_ommatidias_visibiluty=False, show_eyes=False, fill=True):
        if index > len(self._rows):
            index = len(self._rows) - 1
        precedent = self._rows[index]
        beta_A = [int(item) for item in precedent[:self._ommatidia_number]]
        beta_B = [int(item) for item in precedent[self._ommatidia_number:2 * self._ommatidia_number]]
        gObj = float(precedent[2 * self._ommatidia_number + 6])
        xObj = float(precedent[2 * self._ommatidia_number + 7])
        yObj = float(precedent[2 * self._ommatidia_number + 8])
        h = float(precedent[2 * self._ommatidia_number + 9])
        l = float(precedent[2 * self._ommatidia_number + 10])
        if show_ommatidias_visibiluty:
            angle = 360 / self._ommatidia_number
            for i in range(self._ommatidia_number):
                color = 'g' if beta_A[i] else 'lightgrey'
                self._axes.add_patch(patches.Wedge((-h, 0), l * 1000, angle * i, angle * (i + 1), color=color, alpha=0.2))
            for i in range(self._ommatidia_number):
                color = 'g' if beta_B[i] else 'lightgrey'
                self._axes.add_patch(patches.Wedge((h, 0), l * 1000, angle * i, angle * (i + 1), color=color, alpha=0.2))
        self._update_borders(min(-(h + l), (xObj - gObj)), max(h + l, xObj + gObj), yObj + gObj + 10, -l)
        if show_eyes:
            self._visualize_eyes(h, l)
        self._visualize_object(xObj, yObj, gObj, 'blue', fill)

    def _find_equal_byte_scals(self):
        scale_dict = dict()
        for i, row in enumerate(self._rows):
            scale = tuple(row[:2*self._ommatidia_number])
            if scale in scale_dict:
                scale_dict[scale].append(i)
            else:
                scale_dict[scale] = [i]
        scale_dict = [(item, scale_dict[item]) for item in scale_dict if len(scale_dict[item]) >= 1]
        scale_dict = dict(scale_dict)
        scale_dict = {k: v for k, v in sorted(scale_dict.items(), key=lambda item: -len(item[1]))}
        return scale_dict

    def visualize_equals_byte_scals(self, index):
        scale_dict = self._find_equal_byte_scals()
        if index > len(scale_dict):
            index = len(scale_dict) - 1
        objects = scale_dict[list(scale_dict.keys())[index]]
        self.visualize_precedent(objects[0], True, True, fill=False)
        for i in range(1, len(objects)):
            self.visualize_precedent(objects[i], fill=False)

    def visualize_many_equals_byte_scals(self, num):
        scale_dict = self._find_equal_byte_scals()
        if num > len(scale_dict):
            num = len(scale_dict) - 1
        flag = True
        for i in range(num):
            objects = scale_dict[list(scale_dict.keys())[i]]
            if flag:
                self.visualize_precedent(objects[0], show_eyes=True, fill=False)
                flag = False
            for j in range(len(objects)):
                self.visualize_precedent(objects[j], fill=False)

    def show(self):
        plt.axis([self._left, self._right, self._bottom, self._up])
        #plt.xlabel("X")
        #plt.ylabel("Y")
        plt.grid()
        plt.show()

#
# distances = []
# angles = []
# file_path = 'dataset-handmade-diagonal-360.csv'
# with open(file_path) as file:
#     rows = file.readlines()
# rows = [row.split(';') for row in rows]
# #fig1 = plt.figure()
# #axes = fig1.add_subplot(111, aspect='equal')
# for row in rows:
#     distances.append(float(row[724]))
#     angles.append(float(row[725]))
# plt.plot(distances)
# plt.show()


#visualizer = Visualizer(360, 'app/datasets/dataset-full-360_robber.csv')
# visualizer.visualize_equals_byte_scals(2)
#visualizer = Visualizer(360, 'dataset-handmade-diagonal-360.csv')
# d = visualizer._find_equal_byte_scals()
# for key in d:
#     print(len(d[key]), end=' ')
# print()
#print(d)
#visualizer = Visualizer(360, 'dataset-handmade-diagonal-enhance-360 — копия.csv')
visualizer = Visualizer(360, 'dataset-handmade-diagonal-enhance-360.csv')
visualizer.visualize_all(10)
# visualizer.visualize_precedent(300, True, True, True)
# visualizer.show()
# visualizer.visualize_many_equals_byte_scals(24000)
# visualizer.show()

# def paint(row, m):
#     #row = text_row.split(';')
#     beta_A = [int(item) for item in row[:m]]
#     beta_B = [int(item) for item in row[m:2*m]]
#     gObj = float(row[2 * m + 6])
#     xObj = float(row[2 * m + 7])
#     yObj = float(row[2 * m + 8])
#     h = float(row[2 * m + 9])
#     l = float(row[2 * m + 10])
#
#     fig1 = plt.figure()
#     ax1 = fig1.add_subplot(111, aspect='equal')
#     angle = 360 / len(beta_A)
#     for i in range(len(beta_A)):
#         color = 'g' if beta_A[i] else 'lightgrey'
#         ax1.add_patch(
#             patches.Wedge(
#                 (-h, 0),  # (x,y)
#                 l*1000,  # radius
#                 angle * i,  # theta1 (in degrees)
#                 angle * (i + 1),  # theta2
#                 color=color, alpha=0.2
#             )
#         )
#     for i in range(len(beta_B)):
#         color = 'g' if beta_B[i] else 'lightgrey'
#         ax1.add_patch(
#             patches.Wedge(
#                 (h, 0),  # (x,y)
#                 l*1000,  # radius
#                 angle * i,  # theta1 (in degrees)
#                 angle * (i + 1),  # theta2
#                 color=color, alpha=0.2
#             )
#         )
#     ax1.add_patch(plt.Circle((xObj, yObj), gObj, color='r'))
#     #ax1.add_patch(plt.Circle((xObj, yObj), 1, color='r'))
#     ax1.add_patch(plt.Circle((-h, 0), 1, color='black'))
#     ax1.add_patch(plt.Circle((h, 0), 1, color='black'))
#     ax1.add_patch(
#         patches.Wedge(
#             (h, 0),  # (x,y)
#             l,  # radius
#             0,  # theta1 (in degrees)
#             360,  # theta2
#             color='black', alpha=0.1
#         )
#     )
#     ax1.add_patch(
#         patches.Wedge(
#             (-h, 0),  # (x,y)
#             l,  # radius
#             0,  # theta1 (in degrees)
#             360,  # theta2
#             color='black', alpha=0.1
#         )
#     )
#     left = min(-(h+l), (xObj-gObj))
#     right = max(h+l, xObj+gObj)
#     up = yObj + gObj + 10
#     bottom = -l
#     plt.axis([left, right, bottom, up])
#     plt.grid()
#     plt.show()
#
#
# def paint_dict(m):
#     fig1 = plt.figure()
#     ax1 = fig1.add_subplot(111, aspect='equal')
#     angle = 360 / m
#     dataset = []
#     d = dict()
#     with open('app/datasets/dataset-full-18.csv.csv') as file:
#     #with open('app/datasets/dataset-full-360_fixed_g_and_fi.csv') as file:
#         import csv
#         reader = csv.reader(file, delimiter=';')
#         for row in reader:
#             dataset.append(row)
#             a = tuple(row[:36])
#             if a in d:
#                 d[a] += 1
#             else:
#                 d[a] = 0
#     for key in tqdm(d):
#         rows = []
#         for row in dataset:
#             if tuple(row[:720]) == key:
#                 rows.append(row)
#         minY, maxY = 1000, 0
#         gObj = float(rows[0][2 * m + 6])
#         xObj = float(rows[0][2 * m + 7])
#         h = float(rows[0][2 * m + 9])
#         l = float(rows[0][2 * m + 10])
#         if len(rows) < 7:
#             continue
#         for row in rows:
#             yObj = float(row[2 * m + 8])
#             xObj = float(row[2 * m + 7])
#             gObj = float(row[2 * m + 6])
#             ax1.add_patch(plt.Circle((xObj, yObj), gObj, color='red', fill=False))
#             if yObj < minY:
#                 minY = yObj
#             if yObj > maxY:
#                 maxY = yObj
#         # beta_A = rows[0][:m]
#         # beta_B = rows[0][m:2*m]
#         # for i in range(len(beta_A)):
#         #     # color = 'g' if beta_A[i] else 'lightgrey'
#         #     color = 'lightgrey'
#         #     ax1.add_patch(
#         #         patches.Wedge(
#         #             (-h, 0),  # (x,y)
#         #             l,  # radius
#         #             angle * i,  # theta1 (in degrees)
#         #             angle * (i + 1),  # theta2
#         #             color=color, alpha=0.2
#         #         )
#         #     )
#         # for i in range(len(beta_B)):
#         #     #color = 'g' if beta_B[i] else 'lightgrey'
#         #     color = 'lightgrey'
#         #     ax1.add_patch(
#         #         patches.Wedge(
#         #             (h, 0),  # (x,y)
#         #             l,  # radius
#         #             angle * i,  # theta1 (in degrees)
#         #             angle * (i + 1),  # theta2
#         #             color=color, alpha=0.2
#         #         )
#         #     )
#         #ax1.add_patch(plt.Circle((xObj, minY), 0.5, color='red',  edgecolor='black'))
#         #ax1.text(1, (minY+maxY)/2, len(rows), fontsize=10)
#         #ax1.add_patch(plt.Circle((xObj, maxY), 0.5, color='red',  edgecolor='black'))
#         # ax1.add_patch(plt.Circle((xObj, yObj), 1, color='r'))
#         ax1.add_patch(plt.Circle((-h, 0), 1, color='black'))
#         ax1.add_patch(plt.Circle((h, 0), 1, color='black'))
#         break
#     beta_A = rows[0][:m]
#     beta_B = rows[0][m:2 * m]
#     for i in range(len(beta_A)):
#         # color = 'g' if beta_A[i] else 'lightgrey'
#         color = 'grey'
#         ax1.add_patch(
#             patches.Wedge(
#                 (-h, 0),  # (x,y)
#                 l*1000,  # radius
#                 angle * i,  # theta1 (in degrees)
#                 angle * (i + 1),  # theta2
#                 color=color, alpha=0.2
#             )
#         )
#     for i in range(len(beta_B)):
#         # color = 'g' if beta_B[i] else 'lightgrey'
#         color = 'grey'
#         ax1.add_patch(
#             patches.Wedge(
#                 (h, 0),  # (x,y)
#                 l*1000,  # radius
#                 angle * i,  # theta1 (in degrees)
#                 angle * (i + 1),  # theta2
#                 color=color, alpha=0.2
#             )
#         )
#     ax1.add_patch(plt.Circle((h, 0), l, color='black', fill=False))
#     ax1.add_patch(plt.Circle((-h, 0), l, color='black', fill=False))
#     plt.axis([-1000, 1000, -20, 1000])
#     plt.grid()
#     plt.show()
#
#
# def paint_all(rows, m):
#     #row = row.split(';')
#     max_left, max_right, max_up, max_bottom = 0, 0, 0, 0
#     fig1 = plt.figure()
#     ax1 = fig1.add_subplot(111, aspect='equal')
#     angle = 360 / m
#     flag = True
#     minY, maxY = 1000, 0
#     for row in tqdm(rows):
#         beta_A = [int(item) for item in row[:m]]
#         beta_B = [int(item) for item in row[m:2*m]]
#         gObj = float(row[2 * m + 6])
#         xObj = float(row[2 * m + 7])
#         yObj = float(row[2 * m + 8])
#
#         h = float(row[2 * m + 9])
#         l = float(row[2 * m + 10])
#         if flag:
#             for i in range(len(beta_A)):
#                 color = 'g' if beta_A[i] else 'lightgrey'
#                 ax1.add_patch(
#                     patches.Wedge(
#                         (-h, 0),  # (x,y)
#                         l,  # radius
#                         angle * i,  # theta1 (in degrees)
#                         angle * (i + 1),  # theta2
#                         color=color, alpha=0.2
#                     )
#                 )
#             for i in range(len(beta_B)):
#                 color = 'g' if beta_B[i] else 'lightgrey'
#                 ax1.add_patch(
#                     patches.Wedge(
#                         (h, 0),  # (x,y)
#                         l,  # radius
#                         angle * i,  # theta1 (in degrees)
#                         angle * (i + 1),  # theta2
#                         color=color, alpha=0.2
#                     )
#                 )
#             flag = False
#         ax1.add_patch(plt.Circle((xObj, yObj), gObj, color='r'))
#         #ax1.add_patch(plt.Circle((xObj, yObj), 1, color='r'))
#         ax1.add_patch(plt.Circle((-h, 0), 1, color='black'))
#         ax1.add_patch(plt.Circle((h, 0), 1, color='black'))
#         left = min(-(h+l), (xObj-gObj))
#         if left < max_left:
#             max_left = left
#         right = max(h+l, xObj+gObj)
#         if right > max_right:
#             max_right = right
#         up = yObj + gObj + 10
#         if up > max_up:
#             max_up = up
#
#     plt.axis([max_left, max_right, -l, max_up])
#     plt.grid()
#     plt.show()


#row = '0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;1;1;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;1;1;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0.6772504345498983;0.5;156.95565735235192;1.5707963267948966;156.95565735235192;1.5707963267948966;0.05555555555555555;9.610762169231326e-15;156.95565735235192;80.0;20.0'
#d = dict()
# with open('app/datasets/dataset-full-18.csv') as file:
# #with open('app/datasets/dataset-full-360_fixed_g_and_fi.csv') as file:
#     import csv
#     reader = csv.reader(file, delimiter=';')
#     for row in reader:
#         paint(row, 18)
#         a = tuple(row[:36])
#         if a in d:
#             d[a] += 1
#         else:
#             d[a] = 0
# print(len(d))
# k = []
# for key in d:
#     if d[key] > 4000:
#         k = key
# print(d[k])
# dataset = []
# with open('app/dataset-full-360_mape003.csv') as file:
#     import csv
#     reader = csv.reader(file, delimiter=';')
#     for row in reader:
#         paint(row, 360)
#         a = tuple(row[:36])
#         # if a == k:
        #     dataset.append(row)
#paint_all(dataset, 360)
#paint(row, 360)
# paint_dict(18)

