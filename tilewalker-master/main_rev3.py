import random
import logging
import math
import matplotlib.path as mpath
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
from matplotlib import animation
from shapely.geometry import Polygon
import numpy as np
import cProfile
import sys
import csv
import datetime

# plt.style.use('ggplot')
show_animation = False
with_cover = False
max_tile = 35
foot_length = 0.38
min_path = foot_length
default_tile_size = 0.05  # 0.3 Meters
max_path = (max_tile * default_tile_size) - foot_length


def setup_logger(name, log_file,
                 formatter=logging.Formatter('%(asctime)s %(levelname)s %(message)s'),
                 level=logging.INFO):
    """
    Function to setup a generic loggers.

    :param name: name of the logger
    :type name: str
    :param log_file: file of the log
    :type log_file: str
    :param formatter: formatter to be used by the logger
    :type formatter: logging.Formatter
    :param level: level to display
    :type level: int
    :return: the logger
    :rtype: logging.Logger
    """
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


logger = setup_logger('logger', 'tilewalker.log', level=logging.DEBUG)


class Path:

    def __init__(self, min_x=min_path, max_x=max_path, min_y=min_path, max_y=max_path, start_point=None,
                 end_point=None):
        """Creating a random path with start and end point"""
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.start_point = start_point
        self.end_point = end_point
        self.path = [(0, 0), (10.0, 10.0)]

    def generate_random_path(self, N=10, start=(0.0, 0.0)):
        self.path = []

        for n in range(N):
            rand_x = np.random.uniform(self.min_x, self.max_x)
            rand_y = np.random.uniform(self.min_y, self.max_y)
            x = rand_x
            y = rand_y
            self.path.append((x, y))
        return self.path

    def get_the_angle(self):
        """Calculating the slop of first segment in the path"""
        if not (self.start_point and self.end_point):
            self.start_point = self.path[0]
            self.end_point = self.path[1]
        dtx = self.end_point[0] - self.start_point[0]
        dty = self.end_point[1] - self.start_point[1]

        self.degrees_temp = math.degrees(math.atan2(dty, dtx))
        if self.degrees_temp < 0:
            self.degrees_final = self.degrees_temp + 360
        else:
            self.degrees_final = self.degrees_temp
        return self.degrees_final

    def retrieve_middle_points(self, distance=0.1):
        """ Retrieving the points on a line of path between two points start_point and end_point with a specific distance."""
        dt = distance
        x0 = self.start_point[0]
        y0 = self.start_point[1]
        x1 = self.end_point[0]
        y1 = self.end_point[1]
        mps = [(x0, y0)]
        t = 0.1
        # Calculate distance between two points
        d = math.sqrt((math.pow((x1 - x0), 2)) + (math.pow((y1 - y0), 2)))
        # Ratio of distances
        t = dt / d
        while dt < d:
            # The point (xt,yt) with specific distance of previouse point
            xt = ((1 - t) * x0) + t * x1
            yt = ((1 - t) * y0) + t * y1
            x0 = xt
            y0 = yt
            mps.append((xt, yt))
            d = math.sqrt(math.pow((x1 - x0), 2) + math.pow((y1 - y0), 2))
            t = dt / d

        if (x1, y1) not in mps:
            mps.append((x1, y1))

        return mps

    def plot(self, ax, show_animation=show_animation):
        """Plotting the random generated path"""
        x = [xp[0] for xp in self.path]
        y = [yp[1] for yp in self.path]
        if show_animation:
            ax.plot(x, y, 'c')
            ax.plot(x[-1], y[-1], 'r*')
            ax.plot(x[0], y[0], 'r.')


class Cover:

    def __init__(self, rows=max_tile, cols=max_tile, tile_size=default_tile_size, tile_csv=None, feet_csv=None):
        """Initialize our tiled cover that including rows and columns of squares"""
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.cover = []
        self.tile_csv = tile_csv
        self.feet_csv = feet_csv

        if self.tile_csv:
            # Creating CSV file "simulation_tile.csv"
            with open(self.tile_csv, 'w') as csvfile:
                csvwriter1 = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                csvwriter1.writerow(["timestamp", "tile-x", "tile-y", "weight%"])

        if self.feet_csv:
            # Creating CSV file "simulation_feet.csv"
            with open(self.feet_csv, 'w') as csvfile:
                csvwriter1 = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                csvwriter1.writerow(["timestamp", "foot-x", "foot-y", "foot_type"])

    def generate_cover(self):
        """Generating a random tiled cover"""
        self.cover = []
        for x in range(self.rows):
            x *= self.tile_size
            row = []
            for y in range(self.cols):
                y *= self.tile_size
                row.append((x, y))
            self.cover.append(row)

        return self.cover

    def get_tiles(self, min_col, max_col, min_row, max_row):
        """ Get tiles coordinates between a specific row an column
        """
        x_cols = [vline[0][0] for vline in self.cover]
        y_rows = [hline[0][0] for hline in self.cover]
        x_tile = [x for x in x_cols if min_col - self.tile_size < x < max_col + self.tile_size]
        y_tile = [y for y in y_rows if min_row - self.tile_size < y < max_row + self.tile_size]

        tiles = []
        for row_count, y in enumerate(y_tile):
            if row_count == len(y_tile) - 1:
                break
            for col_count, x in enumerate(x_tile):
                if col_count == len(x_tile) - 1:
                    break
                tile = [(x, y), (x, y_tile[row_count + 1]), (x_tile[col_count + 1], \
                                                             y_tile[row_count + 1]),
                        (x_tile[col_count + 1], y_tile[row_count])]
                tiles.append(tile)
        return tiles

    def intersect_area(self, rectangle, which_foot, timestamp):
        """
        Takes as a parameter one rectangle and the cover , and return amount of area
         covered by the foot rectangle on the interested tiles of the cover.
        """
        rect_center = rectangle[-1]
        rectangle = rectangle[:-1]
        rect_x_corners = [x for x, y in rectangle]
        rect_y_corners = [y for x, y in rectangle]
        min_col = min(rect_x_corners)
        max_col = max(rect_x_corners)
        min_row = min(rect_y_corners)
        max_row = max(rect_y_corners)

        tiles = self.get_tiles(min_col, max_col, min_row, max_row)
        tile_overlap_areas = []
        rectangle = [tuple(p) for p in rectangle]
        rect_poly = Polygon(rectangle)
        rect_area = rect_poly.area

        for tile in tiles:
            tile_poly = Polygon(tile)
            area = tile_poly.intersection(rect_poly).area
            polygon = []
            if area:
                tile_x = tile[2][0] / self.tile_size
                tile_y = tile[2][1] / self.tile_size
                wieght_percent = (area * 100) / rect_area
                if self.tile_csv:
                    with open(self.tile_csv, 'a') as csvfile:
                        csvwriter1 = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        csvwriter1.writerow([timestamp, tile_x, tile_y, wieght_percent])

                tile_overlap_areas.append({'tile': tile, 'overlap_area': area})

        return tile_overlap_areas

    def plot(self, path, ax):
        """Plotting the tiled cover"""
        x = [vline[0:self.cols] for vline in self.cover]
        y = [hline[0:self.rows] for hline in self.cover]
        ax.vlines(x, 0.0, self.cover[-1][-1], 'silver', zorder=-1)
        ax.hlines(y, 0.0, self.cover[-1][-1], 'silver', zorder=-1)


class Foot:

    @classmethod
    def get_path_data(cls, path, points):
        """A method to draw a rectangle(foot)"""

        cls.path_data = [
            (path.MOVETO, (points[0][0], points[0][1])),
            (path.LINETO, (points[1][0], points[1][1])),
            (path.LINETO, (points[2][0], points[2][1])),
            (path.LINETO, (points[3][0], points[3][1])),
            (path.CLOSEPOLY, (points[0][0], points[0][1]))
        ]
        return cls.path_data

    def __init__(self, width=0.1, length=foot_length, x=0.0, y=0.0, alpha=0.0):
        """Initialize the parameters in order to create a foot"""
        self.length = length  # ( m )
        self.width = width  # ( m )
        self.alpha = alpha
        self.x = x
        self.y = y
        self.FB = self.length * self.width
        self.to_draw = None
        self.which_foot = 'right'

    def get_points(self):
        """getting the corner points of the rectangle from its center and return the coordinates"""
        p_center = [self.x, self.y]
        p1 = [self.x - (self.length / 2), self.y - (self.width / 2)]
        p2 = [self.x + (self.length / 2), self.y - (self.width / 2)]
        p3 = [self.x + (self.length / 2), self.y + (self.width / 2)]
        p4 = [self.x - (self.length / 2), self.y + (self.width / 2)]
        return [p1, p2, p3, p4, p_center]

    def move(self, x, y, distance, angle, last_moved_foot=0):
        """ Moving a foot from an initial position with a proportion of distance and angle"""
        self.alpha = angle
        angle = np.radians(self.alpha)
        if last_moved_foot == 0:
            self.which_foot = 'right'
            self.x = x + (np.sin(angle) * distance)
            self.y = y - (np.cos(angle) * distance)
        else:
            self.which_foot = 'left'
            self.x = x - (np.sin(angle) * distance)
            self.y = y + (np.cos(angle) * distance)

    def rotate(self, alpha):
        """Rotating a foot, using a module from Matplotlib library"""

        rotated = Affine2D().rotate_deg_around(self.x, self.y, alpha).transform_affine(self.get_points())

        """Here there is another way to rotated a rectangle with a proportion of alpha"""
        # BL = self.x + (self.length / 2) * math.cos(alpha) + (self.width/2) * math.sin(alpha), self.y - (self.width / 2) * math.cos(alpha) + (self.width/2) * math.sin(alpha)
        # BR = self.x - (self.length / 2) * math.cos(alpha) + (self.width/2) * math.sin(alpha), self.y - (self.width / 2) * math.cos(alpha) - (self.width/2) * math.sin(alpha)
        # UR = self.x - (self.length / 2) * math.cos(alpha) - (self.width/2) * math.sin(alpha), self.y + (self.width / 2) * math.cos(alpha) - (self.width/2) * math.sin(alpha)
        # UL = self.x + (self.length / 2) * math.cos(alpha) - (self.width/2) * math.sin(alpha), self.y + (self.width / 2) * math.cos(alpha) + (self.width/2) * math.sin(alpha)
        return rotated

    def plot(self, fig, ax, cover, show_animation=show_animation):
        """Plotting a rectangle(foot) that is already rotated"""
        if self.to_draw:
            self.to_draw.remove()

        m_path = mpath.Path
        points = self.rotate(self.alpha)  # rotated rectangle
        if cover:
            time = datetime.datetime.now()
            cover.intersect_area(points, self.which_foot, time)

            with open(cover.feet_csv, 'a') as csvfile:
                csvwriter1 = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                csvwriter1.writerow([time, points[-1][0], points[-1][1], self.which_foot])

        path_data = self.get_path_data(m_path, points)
        codes, verts = zip(*path_data)
        m_path = mpath.Path(verts, codes)
        x, y = zip(*m_path.vertices)
        if show_animation:
            self.to_draw, = ax.plot(x, y, 'b')
            fig.canvas.draw()
            fig.canvas.flush_events()


class Person:

    def __init__(self, alpha=0.0, step_length=0.3, weight=70.0, vi=1.4, x=0.0, y=0.0, foot_width=0.1):
        """initialize the position and velocity of the person.
            alpha is in degree"""
        self.step_length = step_length  # average_steps
        self.weight = weight
        self.alpha = alpha  # radius
        self.feet_gap = 0.3
        self.foot_width = foot_width
        self.x = x
        self.y = y
        self.vi = vi
        angle = np.radians(self.alpha)
        rfx = self.x + (np.sin(angle) * (self.feet_gap / 2))
        rfy = self.y - (np.cos(angle) * (self.feet_gap / 2))
        lfx = self.x - (np.sin(angle) * (self.feet_gap / 2))
        lfy = self.y + (np.cos(angle) * (self.feet_gap / 2))

        self.right_foot = Foot(x=rfx, y=rfy, alpha=alpha)
        self.left_foot = Foot(x=lfx, y=lfy, alpha=alpha)
        self.last_moved_foot = 0  # 0 = foot_left , 1 = foot_right
        self.epsilon = (self.step_length / 2) + 0.1
        self.vx = self.vi * np.cos(self.alpha * np.pi / 180)
        self.vy = self.vi * np.sin(self.alpha * np.pi / 180)
        self.a = 0.68  # m/s2

    def step(self):
        """Person taking a step forward by moving a foot in order to follow the path"""
        if self.last_moved_foot == 0:
            # update the position of the right foot
            self.right_foot.move(self.x, self.y, (self.feet_gap / 2), self.alpha, self.last_moved_foot)

        else:
            # update the position of the left foot
            self.left_foot.move(self.x, self.y, (self.feet_gap / 2), self.alpha, self.last_moved_foot)

    def plot(self, fig, ax, cover, stand_mode=False):
        """Plotting both foots of person"""
        # The person is standing
        if stand_mode:
            self.right_foot.which_foot = 'right'
            self.right_foot.plot(fig, ax, cover)
            self.left_foot.which_foot = 'left'
            self.left_foot.plot(fig, ax, cover)

        # The person is walking
        elif self.last_moved_foot == 0:
            self.right_foot.plot(fig, ax, cover)
            self.last_moved_foot = 1

        else:
            self.left_foot.plot(fig, ax, cover)
            self.last_moved_foot = 0

    def walk(self, path, cover, fig, ax, with_cover=False):
        """Person start to walk by taking steps"""
        cx = [xp[0] for xp in path.path]
        cy = [yp[1] for yp in path.path]
        lastIndex = len(cx) - 1

        target_ind = 0
        while lastIndex >= target_ind:

            if target_ind > 0:
                path.start_point = (cx[target_ind - 1], cy[target_ind - 1])
                path.end_point = (cx[target_ind], cy[target_ind])
                path.get_the_angle()
                alpha = path.degrees_final
                mps = path.retrieve_middle_points(self.step_length)
                for counter, p in enumerate(mps):
                    logger.debug('counter {} p {}'.format(counter, p))

                    if counter == 0 and target_ind == 1:
                        continue

                    self.x = p[0]
                    self.y = p[1]
                    self.alpha = alpha
                    # Walking mode
                    self.step()
                    self.plot(fig, ax, cover)
                    if show_animation:
                        plt.pause(0.2)

            if target_ind == 0 or target_ind == lastIndex:
                # Standing mode
                self.plot(fig, ax, cover, stand_mode=True)
                if show_animation:
                    plt.pause(0.2)

            target_ind += 1

        self.step()
        self.plot(fig, ax, cover)


def press(event):
    if event.key == 'q' or event.key == 'Q':
        print('Quitting upon request.')
        sys.exit(0)


def main():
    logger.debug('tilewalker started')
    # for stopping simulation with key.
    if show_animation:
        fig, ax = plt.subplots()
        fig.canvas.mpl_connect('key_press_event', press)
    else:
        fig = None
        ax = None

    """start moving the foots from t=0 to t=t_end in steps of dt"""
    path = Path()
    path.generate_random_path(N=10)
    path.get_the_angle()

    try:
        tile_csv = sys.argv[1]
    except:
        tile_csv = 'simulation_tile.csv'
    try:
        feet_csv = sys.argv[2]
    except:
        feet_csv = 'simulation_feet.csv'

    cover = Cover(tile_csv=tile_csv, feet_csv=feet_csv)
    cover.generate_cover()

    x = path.path[0][0]
    y = path.path[0][1]
    alpha = path.degrees_final
    v = 0.0

    if with_cover:
        cover.plot(path, ax)
    path.plot(ax)
    person = Person(x=x, y=y, alpha=alpha, vi=v)
    person.walk(path, cover, fig, ax)

    if show_animation:
        plt.show()


if __name__ == '__main__':
    # cProfile.run('main()')
    main()

