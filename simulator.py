from scipy import misc
import math
from data.simple_room import LINES
from data.render import render
from Raycaster import Raycaster


RED = 0
GREEN = 1
BLUE = 2


class Simulator(object):
    def __init__(self):
        self.simulation_steps_per_meter = 100
        self.map = render(LINES)
        self.pixels_per_meter = 100
        self.simulation_steps_per_radian = 1.0 / math.radians(9)
        self.map_height, self.map_width, self.colors = self.map.shape
        self.raycaster = Raycaster(LINES, max(self.map_height, self.map_width))

    def reward(self, robot, robot_size, collison_reward, step_reward):
        x = robot.x
        y = robot.y

        ix = int(x * self.pixels_per_meter)
        iy = int(y * self.pixels_per_meter)
        if ix < 0 or ix >= self.map_width or iy < 0 or iy >= self.map_height:
            return collison_reward

        for i in range(int(robot_size * self.pixels_per_meter * 2)):
            for j in range(int(robot_size * self.pixels_per_meter * 2)):
                ioff = i - int(self.pixels_per_meter * robot_size)
                joff = j - int(self.pixels_per_meter * robot_size)
                if ioff * ioff + joff * joff < int(robot_size * self.pixels_per_meter) * int(robot_size * self.pixels_per_meter):
                    ix = int(x * self.pixels_per_meter) + ioff
                    iy = int(y * self.pixels_per_meter) + joff
                    if 0 <= ix < self.map_width and 0 <= iy < self.map_height:
                        if self.map[self.map_height - iy - 1][ix][0] < 10:
                            return collison_reward
        return step_reward

    def video(self, robot):
        return None

    def sense(self, robot):
        measurements = []
        for i in robot.sensors:
            measurements.append(self.sense_cone(robot, i))
        return measurements

    def action(self, act):
        return act

    def sense_cone(self, robot, sensor, relative_angle=0):
        angle_steps = max(1, int(sensor.cone_width * self.simulation_steps_per_radian))
        min_val = sensor.max_range

        for alpha in range(angle_steps):
            angle = robot.heading + sensor.heading + relative_angle + (alpha - int(angle_steps / 2.0)) / self.simulation_steps_per_radian

            p = self.raycaster.cast((robot.x, robot.y, angle))
            dx = p[0] - robot.x
            dy = p[1] - robot.y
            dist = math.sqrt(dx * dx + dy * dy)
            min_val = min(min_val, dist)

        return sensor.max_range if min_val == sensor.max_range else min_val
