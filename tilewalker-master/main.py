import random
import math
import matplotlib.path as mpath
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
from matplotlib import animation
import numpy as np
#plt.style.use('ggplot')
show_animation = True





class Path:
    """Creating a random path with start and end point"""
    def __init__(self, min_x=0.0, max_x=10.0, min_y=0.0, max_y=10.0, start_point=None, end_point=None):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.start_point = start_point
        self.end_point = end_point
        self.path = [(0, 0), (10.0, 10.0)]

    def generate_random_path(self, N = 10, start=(0.0, 0.0)):
        self.path = []

        for n in range(N):
            rand_x = np.random.uniform(self.min_x, self.max_x)
            rand_y = np.random.uniform(self.min_y, self.max_y)
            x = rand_x
            y = rand_y
            self.path.append((x, y))
        return self.path

#    def get_the_angle(self):
    def get_the_angle(self):
        """Calculating the slop of first segment in the path"""
        # for m in range(len(self.generate_random_path())-1):
        #dtx = self.path[1][0] - self.path[0][0]
        #dty = self.path[1][1] - self.path[0][1]
        if not(self.start_point and self.end_point):
            self.start_point = self.path[0]
            self.end_point = self.path[1]
        dtx = self.end_point[0] - self.start_point[0]
        dty = self.end_point[1] - self.start_point[1]
            
        self.degrees_temp = math.degrees(math.atan2(dty,dtx))
        if self.degrees_temp < 0:
            self.degrees_final = self.degrees_temp + 360
        else:
            self.degrees_final = self.degrees_temp
        return self.degrees_final

                        
    def retrieve_middle_points(self, distance=0.1):
        """ Retrieving the points on a line between two points start_point and end_point with a specific distance."""
        dt = distance
        x0 = self.start_point[0]
        y0 = self.start_point[1]
        x1 = self.end_point[0]
        y1 = self.end_point[1]
        mps = [(x0,y0)]
        t = 0.1
        # Calculate distance between two points
        d = math.sqrt((math.pow((x1-x0),2))+(math.pow((y1-y0),2)))
        # Ratio of distances
        t = dt/d 
        while dt < d :
            # The point (xt,yt) with specific distance of previouse point
            xt = ((1-t)*x0) + t*x1
            yt = ((1-t)*y0) + t*y1
            x0 = xt
            y0 = yt
            mps.append((xt,yt))
            d = math.sqrt(math.pow((x1-x0),2)+math.pow((y1-y0),2))
            t = dt/d 
        
        if (x1,y1) not in mps:
            mps.append((x1,y1))    
            
        return mps 



    def plot(self):
        """Plotting the random generated path"""
        plt.cla()
        # for stopping simulation with the esc key.
        plt.gcf().canvas.mpl_connect('key_release_event',
            lambda event: [exit(0) if event.key == 'escape' else None])

        x = [xp[0] for xp in self.path]
        y = [yp[1] for yp in self.path]
        plt.plot(x, y, 'c')
        plt.plot(x[-1], y[-1], 'r*')
        plt.plot(x[0], y[0], 'r.')
        #print(path.path)

"""
path = Path()
path.generate_random_path()
path.get_the_angle()
"""

class Cover:
    """Initialize our tiled cover that including rows and columns of squares"""
    def __init__(self, rows=35, cols=35, tile_size=0.3):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.cover = []
    """Generating a random tiled cover"""
    def generate_cover(self):
        self.cover = []
        for x in range(self.rows):
            x *= self.tile_size
            row = []
            for y in range(self.cols):
                y *= self.tile_size
                row.append((x, y))
            self.cover.append(row)

        return self.cover
    """Plotting the tiled cover"""
    def plot(self, path):
        x = [vline[0:self.cols] for vline in self.cover]
        y = [hline[0:self.rows] for hline in self.cover]
        plt.vlines(x, path.min_x, self.cover[-1][-1],'silver')
        plt.hlines(y, path.min_y, self.cover[-1][-1],'silver')

"""
cover = Cover()
c = cover.generate_cover()
"""


class Foot:
    """A method to draw a rectangle(foot)"""
    @classmethod
    def get_path_data(cls, path, points):

        cls.path_data = [
            (path.MOVETO, (points[0][0], points[0][1])),
            (path.LINETO, (points[1][0], points[1][1])),
            (path.LINETO, (points[2][0], points[2][1])),
            (path.LINETO, (points[3][0], points[3][1])),
            (path.CLOSEPOLY, (points[0][0], points[0][1]))
            ]
        return cls.path_data

    def __init__(self, width=0.1, length=0.38, x=0.0, y=0.0, alpha=0.0):
        """Initialize the parameters in order to create a foot"""
        self.length = length  # ( m )
        self.width = width  # ( m )
        self.alpha = alpha
        self.x = x
        self.y = y
        self.FB = self.length * self.width

    """getting the corner points of the rectangle from its center and return the coordinates"""
    def get_points(self):
        p_center = [self.x, self.y]
        p1 = [self.x - self.length / 2, self.y - self.width / 2]
        p2 = [self.x + self.length / 2, self.y - self.width / 2]
        p3 = [self.x + self.length / 2, self.y + self.width / 2]
        p4 = [self.x - self.length / 2, self.y + self.width / 2]
        #print([p1, p2, p3, p4, p_center])

        return [p1, p2, p3, p4, p_center]

    """ Moving a foot from an initial position with a proportion of distance and angle"""
    def move(self, x, y, distance, angle, last_moved_foot=0):
        self.alpha = angle
        angle = np.radians(self.alpha)
        if last_moved_foot == 0:
            self.x = x+(np.sin(angle) * distance)
            self.y = y-(np.cos(angle) * distance)
        else:
            self.x = x-(np.sin(angle) * distance)
            self.y = y+(np.cos(angle) * distance)

               
        """self.x += np.cos(angle) * distance
        self.y += np.sin(angle) * distance
        return self.x, self.y"""
    
    """Rotating a foot, using a module from Matplotlib library"""
    def rotate(self,alpha):
        rotated = Affine2D().rotate_deg_around(self.x,self.y,alpha).transform_affine(self.get_points())

        """Here there is another way to rotated a rectangle with a proportion of alpha"""
        # BL = self.x + (self.length / 2) * math.cos(alpha) + (self.width/2) * math.sin(alpha), self.y - (self.width / 2) * math.cos(alpha) + (self.width/2) * math.sin(alpha)
        # BR = self.x - (self.length / 2) * math.cos(alpha) + (self.width/2) * math.sin(alpha), self.y - (self.width / 2) * math.cos(alpha) - (self.width/2) * math.sin(alpha)
        # UR = self.x - (self.length / 2) * math.cos(alpha) - (self.width/2) * math.sin(alpha), self.y + (self.width / 2) * math.cos(alpha) - (self.width/2) * math.sin(alpha)
        # UL = self.x + (self.length / 2) * math.cos(alpha) - (self.width/2) * math.sin(alpha), self.y + (self.width / 2) * math.cos(alpha) + (self.width/2) * math.sin(alpha)
        return rotated
    """Plotting a rectangle(foot) that is already rotated"""
    def plot(self):
        m_path = mpath.Path
        points = self.rotate(self.alpha)  # rotated rectangle
        path_data = self.get_path_data(m_path, points)
        codes, verts = zip(*path_data)
        m_path = mpath.Path(verts, codes)
        x, y = zip(*m_path.vertices)
        plt.plot(x, y, 'b')
        #plt.plot(self.x, self.y, 'g.')


#foot = Foot()


class Person:
    """initialize the position and velocity of the person.
            alpha is in degree"""

    def __init__(self, alpha=0.0, step_length=0.3, weight=70.0, vi=1.4, x=0.0, y=0.0, foot_width=0.1):
        self.step_length = step_length  # average_steps
        self.weight = weight
        self.alpha = alpha # radius
        self.feet_gap = 0.3
        self.foot_width = foot_width
        self.x = x
        self.y = y
        self.vi = vi
        angle = np.radians(self.alpha)
        rfx = self.x+(np.sin(angle) * (self.feet_gap/2))
        rfy = self.y-(np.cos(angle) * (self.feet_gap/2))
        lfx = self.x-(np.sin(angle) * (self.feet_gap/2))
        lfy = self.y+(np.cos(angle) * (self.feet_gap/2))
        
        self.right_foot = Foot(x=rfx, y=rfy, alpha=alpha)
        self.left_foot = Foot(x=lfx, y=lfy, alpha=alpha)
        self.last_moved_foot = 0  # 0 = foot_left , 1 = foot_right
        self.epsilon = (self.step_length / 2) + 0.1
        self.vx = self.vi * np.cos(self.alpha * np.pi / 180)
        self.vy = self.vi * np.sin(self.alpha * np.pi / 180)
        self.a = 0.68  # m/s2
    
    """Calculating the pressure of one foot exerted on the tiles
    def force(self):
        We have three different pressure exerted by one foot
        1) bottom part of foot
        2) mid part
        3) front part
        """
        
        #self.area = 0.12 * 0.27  # bottom of the person's foot assuming 12cm wide and 27 long
        #self.pressure = round(person.weight / self.area)  # pressure is obtained through dividing the weight of person by the area of footprint(rectangle)
        #return self.pressure
        
    """rotate the direction of person when the path direction is changed"""
    #def rotate(self,alpha):
        #pass
        # self.right_foot.x = self.right_foot.x * math.cos(alpha) - self.right_foot.y * math.sin(alpha)
        # self.right_foot.y = self.right_foot.x * math.sin(alpha) + self.right_foot.y * math.cos(alpha)
        # self.left_foot.x = self.left_foot.x * math.cos(alpha) - self.left_foot.y * math.sin(alpha)
        # self.left_foot.y = self.left_foot.x * math.sin(alpha) + self.left_foot.y * math.cos(alpha)
        # return self.right_foot.x, self.right_foot.y, self.left_foot.x, self.left_foot.y
    """Person taking a step forward by moving a foot in order to follow the path"""
    def step(self):
        if self.last_moved_foot == 0:
            self.right_foot.move(self.x, self.y, (self.feet_gap/2), self.alpha, self.last_moved_foot)
            self.last_moved_foot = 1
            
        else:
            self.left_foot.move(self.x, self.y, (self.feet_gap/2), self.alpha, self.last_moved_foot)
            self.last_moved_foot = 0
        """
        # dt = 1
        # ns = np.array(self.v) * dt/self.step_length
        # print(ns)
        if 90 <= self.path.degrees_final <= 270:

            if self.last_moved_foot == 1:

                self.right_foot.move(self.step_length,math.radians(self.path.degrees_final))

        # update the position of the right foot

            else:
                self.left_foot.move(self.step_length,math.radians(self.path.degrees_final))
        """
    # update the position of the left foot
    """plotting both foots of person"""
    def plot(self):
        self.right_foot.plot()
        self.left_foot.plot()
    """calculate the distance between tow way points"""
    """
    @staticmethod
    def distance(x, y, destX, destY):
        distance = math.sqrt((destX - x) ** 2 + (destY - y) ** 2)
        return distance
    """
    """person start to walk by taking steps"""
    def walk(self, path, cover, with_plot=True):
        cx = [xp[0] for xp in path.path]
        cy = [yp[1] for yp in path.path]
        lastIndex = len(cx) - 1

        target_ind = 0
        while lastIndex >=  target_ind:

            if show_animation: 
                
                if target_ind > 0 :
                    path.start_point = (cx[target_ind-1],cy[target_ind-1])
                    path.end_point = (cx[target_ind], cy[target_ind])
                    path.get_the_angle()
                    alpha=path.degrees_final
                    mps = path.retrieve_middle_points(self.step_length)
                    for counter, p in enumerate(mps):
                        
                        if counter == 0 and target_ind == 1:
                            continue

                        path.plot()
                        cover.plot(path)
                        self.x = p[0]
                        self.y = p[1]
                        self.alpha = alpha
                        self.step()
                        self.plot()
                        plt.pause(0.2)
                        if (counter == len(mps)-2 and not target_ind == lastIndex):
                           path.plot()
                           cover.plot(path)
                           self.step()
                           self.plot()
                           plt.pause(0.2)
                           break                            

                if target_ind == 0:
                    path.plot()
                    cover.plot(path)
                    self.plot()
                    plt.pause(1)

                   
                plt.pause(0.2)
                target_ind += 1
                
        self.step()             
        """
        if len(path.path) < 2:
            return
        (self.x, self.y) = path.path[0]
        # set the direction
        for dest in path.path[1:]:

            #checking the condition that says if the person arrived at the specific area of a next way point change 
            #the direction and follow the new segment of path till reach the new way point's are

            while self.distance(self.x, self.y, dest[0], dest[1]) < self.epsilon:
                self.step()
                if with_plot:
                    self.plot(fig)

            # if I'm here, that means that I reached the destination
            # now:
            # 1) set the new destination
            # 2) turn towards the new destination, changing the direction
        """

#person = Person()

"""
def simulation():
    pass


def update(self,x_i, y_i, vx_i, vy_i,t,dt):
        update scheme that advances the person forward in time by dt in order
        to track the path
        vx_f = vx_i + person.a * dt
        vy_f = vy_i + person.a * dt
        x_f = x_i + person.vi * dt
        y_f = y_i + person.vi * dt

        What happens if the person reaches to the next way point

        for i in range(len(path.path[1:])):
            current_start = [i]
            current_end = [i+1]
            i += 1

            if person.alpha != path.degrees_final:
                dtx = current_end[0] - current_start[0]
                dty = current_end[1] - current_start[1]
                degrees_temp = math.degrees(math.atan2(dty, dtx))
                if degrees_temp < 0:
                    degrees_final = degrees_temp + 360
                else:
                    degrees_final = degrees_temp

                dtx_new = dtx / vx_i
                dty_new = dty / vy_i
                self.vx_f = (vx_i*dtx_new)
                self.vy_f = (vy_i * dty_new)
                self.x_f = x_i + vx_i * dtx_new
                self.y_f = y_i + vy_i * dty_new
                # t =
            else:
                # t =
                return degrees_final, self.vx_f, self.x_f, self.y_f, self.vy_f, t
"""
"""
fig = plt.figure()
# print(path.path)
print(path.degrees_final)
# print(person.rotate(math.radians(50)))
print(c)
"""

"""def plot_figure():

    path.plot()
    cover.plot(fig)
    person.plot(fig)
    plt.show()
"""
    
def main():
    """start moving the foots from t=0 to t=t_end in steps of dt"""
    path = Path() 
    path.generate_random_path()
    path.get_the_angle()

    cover = Cover()
    cover.generate_cover()
    
    # simulation time
    #dt = 0.1
    #iteration_time = 15.0

    x = path.path[0][0]
    y = path.path[0][1]
    alpha=path.degrees_final
    #alpha = math.radians(45.0)
    v = 0.0
    # person
    person = Person(x=x, y=y, alpha=alpha, vi=v)
    person.walk(path, cover)
    """for n in range(10):
        person.step()
        person.plot()"""
    #if show_animation:
     #   plot_figure()

    if show_animation: 
        path.plot()
        cover.plot(path)
        person.plot()
        plt.pause(1)
        plt.show()


if __name__ == '__main__':
    main()
