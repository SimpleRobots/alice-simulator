import math
import simulator

MAX_SPEED_LEFT = 0.1142 * 2
MAX_SPEED_RIGHT = 0.1142 * 2
WHEELBASE = 0.2

class Sensor(object):
    def __init__(self, x, y, max_range, cone_width, heading):
        self.x = x
        self.y = y
        self.max_range = max_range
        self.cone_width = cone_width
        self.heading = heading


class Robot(object):
    def __init__(self, x, y, heading, sensors):
        self.x = x
        self.y = y
        self.heading = heading
        self.sensors = sensors


class AliceBot(object):
    def __init__(self, visualisation):
        sensors = [Sensor(0.12, 0.08, 2, math.radians(30), math.radians(45)),
                   Sensor(0.14, 0.04, 2, math.radians(30), math.radians(15)),
                   Sensor(0.14, -0.04, 2, math.radians(30), math.radians(-15)),
                   Sensor(0.12, -0.08, 2, math.radians(30), math.radians(-45))]  # ,
        # Sensor(-0.15, 0, 2, math.radians(30), math.radians(-180))]
        initial_action = [0.2, 0]
        self.actions = [(0.2, -2), (0.2, 0), (0.2, 2)]
        self.action_dimension = 2

        self.state_size = len(sensors)

        self.visualisation = visualisation

        x = 1
        y = 1
        heading = 0
        self.environment = simulator.Simulator()

        self.robot = Robot(x, y, heading, sensors)
        self.wheel_distance = WHEELBASE
        self.size = 0.15

    def get_video(self):
        return self.environment.video(self.robot)

    def get_measurements(self):
        return self.environment.sense(self.robot)

    def get_state(self):
        return self.get_measurements()

    def get_pose(self):
        return [self.robot.x, self.robot.y, self.robot.heading]

    def reset(self):
        self.set_pose(1, 1, 0)

    def set_pose(self, x, y, heading):
        self.robot.x = x
        self.robot.y = y
        self.robot.heading = heading

    def act(self, action, dt=0.1):
        action = self.environment.action(action)
        v_left = max(-MAX_SPEED_LEFT, min(MAX_SPEED_LEFT, action[0]))
        v_right = max(-MAX_SPEED_RIGHT, min(MAX_SPEED_RIGHT, action[1]))

        v_avg = 1.0 / 2.0 * (v_left + v_right)
        dx = math.cos(self.robot.heading) * v_avg
        dy = math.sin(self.robot.heading) * v_avg
        dtheta = 1.0 / self.wheel_distance * (v_right - v_left)

        self.robot.x += dx * dt
        self.robot.y += dy * dt
        self.robot.heading += dtheta * dt

        while self.robot.heading > math.pi:
            self.robot.heading -= 2 * math.pi
        while self.robot.heading <= -math.pi:
            self.robot.heading += 2 * math.pi

        self.visualisation.broadcast(self)

        return action, self.environment.reward(self.robot, self.size, -100, 1)
