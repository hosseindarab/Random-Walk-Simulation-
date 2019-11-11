import random
import math
import matplotlib.path as mpath
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import numpy as np
#plt.style.use('ggplot')


class Path:
    def __init__(self, min_x=0.0, max_x=10.0, min_y=0.0, max_y=10.0):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.path = [(0, 0), (10.0, 10.0)]

    def generate_random_path(self, N = 10, start=(0.0, 0.0)):
        self.path = [start]

        for n in range(1, N):
            rand_x = np.random.uniform(self.min_x, self.max_x)
            rand_y = np.random.uniform(self.min_y, self.max_y)
            x = rand_x
            y = rand_y
            self.path.append((x, y))
        return self.path

    def get_the_angle(self):

        angles = []

        for m in range(len(self.generate_random_path())-1):
            dtx = self.path[m+1][0] - self.path[m][0]
            dty = self.path[m+1][1] - self.path[m][1]
            degrees_temp = math.degrees(math.atan2(dty,dtx))
            if degrees_temp < 0:
                degrees_final = degrees_temp + 360
            else:
                degrees_final = degrees_temp
            angles.append(degrees_final)
        return angles

    def plot(self, fig):
        p = Path()
        path = p.generate_random_path(8)
        x = [xp[0] for xp in path]
        y = [yp[1] for yp in path]
        plt.plot(x, y, 'c',figure=fig)
        plt.plot(x[-1], y[-1], 'r*',figure=fig)


# p = Path()
#
# print(p.get_the_angle())
# print(p.generate_random_path())


class Cover:

    def __init__(self, rows=34, cols=34, tile_size=0.3):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.cover = []

    def generate_cover(self):

        self.cover = []
        for x in range(self.rows + 1):
            x *= self.tile_size

            row = []

            for y in range(self.cols + 1):
                y *= self.tile_size
                row.append((x, y))
            self.cover.append(row)

        return self.cover

    def plot(self, fig):
        x = [vline[0:self.cols] for vline in c]
        y = [hline[0:self.rows] for hline in c]
        plt.vlines(x, path.min_x, c[-1][-1],'silver',figure=fig)
        plt.hlines(y, path.min_y, c[-1][-1],'silver',figure=fig)


cover = Cover()
c = cover.generate_cover()
# fig= plt.figure()
# cols = cover.cols
# rows = cover.rows
# x = [vline[0:cols] for vline in c]
# y = [hline[0:rows] for hline in c]
# plt.vlines(x,c[0][0],c[-1][-1])
# plt.hlines(y,c[0][0],c[-1][-1])
# plt.show()

print(c)


class Foot:

    def __init__(self, width=0.1, length=0.4, x=0.0, y=0.0):
        self.length = length  # ( m )
        self.width = width  # ( m )
        self.alpha = 45
        self.x = x
        self.y = y

    def get_points(self):
        p_center = [self.x, self.y]
        p1 = [self.x - self.length / 2, self.y - self.width / 2]
        p2 = [self.x + self.length / 2, self.y - self.width / 2]
        p3 = [self.x + self.length / 2, self.y + self.width / 2]
        p4 = [self.x - self.length / 2, self.y + self.width / 2]

        # p5 = [p4[0], self.feet_gap + p4[1]]
        # p6 = [p3[0], p3[1] + self.feet_gap]
        # p7 = [p6[0], p6[1]+self.width]
        # p8 = [p5[0], p5[1]+self.width]
        # p_center2 = [(p5[0]+p6[0])/2, (p5[1]+p8[1])/2]

        return [p1, p2, p3, p4, p_center]

    def get_path_data(self, path, points):

        path_data = [
            (path.MOVETO, (points[0][0], points[0][1])),
            (path.LINETO, (points[1][0], points[1][1])),
            (path.LINETO, (points[2][0], points[2][1])),
            (path.LINETO, (points[3][0], points[3][1])),
            (path.CLOSEPOLY, (points[0][0], points[0][1]))
            ]

        # path_data2 = [
        #
        #     (path.MOVETO, (points[4][0], points[4][1])),
        #     (path.LINETO, (points[5][0], points[5][1])),
        #     (path.LINETO, (points[6][0], points[6][1])),
        #     (path.LINETO, (points[7][0], points[7][1])),
        #     (path.CLOSEPOLY, (points[4][0], points[4][1]))
        #
        # ]
        # path_data =[path_data1,path_data2]
        return path_data

    def move(self, distance):
        self.x = self.x + (math.cos(math.pi*2) * distance)
        self.y = self.y + (math.sin(math.pi*2) * distance)
        return self.x, self.y

    def rotate(self, alpha):
        rotated = Affine2D().rotate_deg_around(x=self.x, y=self.y, degrees=alpha).transform_affine(self.get_points())
        return rotated

        # p1 = [self.get_points()[0][0] + distance, self.get_points()[0][1] + distance]
        # p2 = [self.get_points()[1][0] + distance, self.get_points()[1][1] + distance]
        # p3 = [self.get_points()[2][0] + distance, self.get_points()[2][1] + distance]
        # p4 = [self.get_points()[3][0] + distance, self.get_points()[3][1] + distance]
        # p_center1 = [self.get_points()[4][0] + distance, self.get_points()[4][1] + distance]

    # def get_new_path_data(self,path , new_points):
    #
    #     new_path_data = [
    #         (path.MOVETO, (new_points[0][0], new_points[0][1])),
    #         (path.LINETO, (new_points[1][0], new_points[1][1])),
    #         (path.LINETO, (new_points[2][0], new_points[2][1])),
    #         (path.LINETO, (new_points[3][0], new_points[3][1])),
    #         (path.CLOSEPOLY, (new_points[0][0], new_points[0][1]))
    #     ]
    #     return new_path_data

    def plot(self, fig):

        path = mpath.Path
        points = self.get_points()
        path_data = self.get_path_data(path, points)
        codes, verts = zip(*path_data)
        path = mpath.Path(verts, codes)
        x, y = zip(*path.vertices)
        plt.plot(x, y, 'b', figure=fig)



        # verts1 = Affine2D().rotate_around(x=self.get_points()[4][0], y=self.get_points()[4][1],
        #                                   theta=self.alpha[0]).transform_affine(verts)
        # path1 = mpath.Path(verts1, codes)
        # x, y = zip(*path1.vertices)

        # codes, new_verts = zip(*new_path_data)
        # new_path = mpath.Path(new_verts, codes)
        # # new_x, new_y = zip(*new_path.vertices)
        #
        # new_verts1 = Affine2D().rotate_around(x=self.move()[4][0], y=self.move()[4][1],
        #                                   theta=self.alpha[0]).transform_affine(new_verts)
        # new_path1 = mpath.Path(new_verts1, codes)
        # self.new_x1, self.new_y1 = zip(*new_path1.vertices)

        # codes, verts2 = zip(*path_data[1])
        # path3 = mpath.Path(verts2, codes)
        # x2, y2 = zip(*path3.vertices)

        # ax.plot(x, y, 'g')
        # ax.plot(new_x, new_y, 'g')
        # plt.plot(self.get_points()[8][0], self.get_points()[8][1], 'r.', markersize=2)

        # plt.plot(self.new_x1, self.new_y1, 'red',figure=fig)
        # ax.plot(self.get_points()[4][0], self.get_points()[4][1], 'k.', markersize=2)
        # ax.plot(verts5[0], verts5[1], 'k.', markersize=2)
        # ax.plot(x2, y2, 'g')
        # plt.plot(self.get_points()[9][0], self.get_points()[9][1], 'r.', markersize=2)
        # ax.plot(self.x3, self.y3, 'red')


class Person:

    def __init__(self, step_length=0.6,weight=70, v=1.4):
        self.step_length = step_length  # average_steps
        self.weight = weight
        self.alpha = path.get_the_angle()  # radius
        self.feet_gap = 0.5
        self.x = self.feet_gap/2 * math.cos(math.pi*2)
        self.y = self.feet_gap/2 * math.sin(math.pi*2)
        # self.v = [v]
        self.right_foot = Foot(x=0, y=-self.feet_gap/2-foot.width/2)#[foot.get_points()[4][0], foot.get_points()[4][1]]
        self.left_foot = Foot(x=0, y=self.feet_gap/2 + foot.width/2)#[self.right_foot[0], self.right_foot[1] + self.feet_gap + Foot().width * 2]
        self.last_moved_foot = 0  # 0 = foot_left , 1 = foot_right
        self.epsilon = self.step_length / 2 + 0.1
    def force(self):
        x = 0
        if self.weight > 0.0:
            x += self.weight * 9.8
            return x

    def rotate(self):
        rotate = 0
        for i in range(len(path.get_the_angle())):
            rotate = Affine2D().rotate_around(x=self.x, y=self.y, theta=i).transform(person.x)
        return rotate

    def step(self):

        # dt = 1
        # ns = np.array(self.v) * dt/self.step_length
        # print(ns)

        if self.last_moved_foot == 1:

            self.right_foot.move(self.step_length)

        # update the position of the right foot

        else:
            self.left_foot.move(self.step_length)

    # update the position of the left foot

    def plot(self, fig):
        self.right_foot.plot(fig)
        self.left_foot.plot(fig)

    def walk(self, with_plot=True):

        distance = path.generate_random_path()[1] - (self.x, self.y)
        if len(path.generate_random_path()) < 2:
            return
        (self.x, self.y) = path.generate_random_path()[0]
        # set the direction
        for dest in path.generate_random_path()[1:]:
            while distance(self.x, self.y, dest[1][0], dest[1][1]) < self.epsilon:
                self.step()
                if with_plot:
                    self.plot(fig)

            # if I'm here, that means that I reached the destination
            # now:
            # 1) set the new destination
            # 2) turn towards the new destination, changing the direction


cover = Cover()
path = Path()
foot = Foot()
person = Person(step_length=0.1)
# cover.draw()
for n in range(10):

    person.step()

# ax.set(xlim=(0, 4), ylim=(0, 4))
fig = plt.figure()
path.plot(fig)
cover.plot(fig)
# foot.plot(fig)
person.plot(fig)
#foot.move()
#person.walk(True)
plt.show()