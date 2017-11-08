import math
import simulator

MAX_SPEED_LEFT = 0.1142 * 2
MAX_SPEED_RIGHT = 0.1142 * 2
WHEELBASE = 0.2

# wheel velocities are multiplied with this factor to introduce a systematic error
BIAS_RIGHT = 1.02
BIAS_LEFT = 0.99

RADIUS_EARTH = 6378000


class Sensor(object):
    def __init__(self, x, y, max_range, cone_width, heading):
        self.x = x
        self.y = y
        self.max_range = max_range
        self.cone_width = cone_width
        self.heading = heading


class Robot(object):
    def __init__(self, x, y, heading, sensors, leds, reference_lat=49.02356, reference_lon=8.43168):
        self.x = x
        self.y = y
        self.heading = heading
        self.predicted_x = x
        self.predicted_y = y
        self.predicted_heading = heading
        self.sensors = sensors
        self.leds = leds
        self.accuracy = 0.01 # 1cm precision
        self.ref_lat = reference_lat
        self.ref_lon = reference_lon

    def get_local_position(self):
        return (self.predicted_x, self.predicted_y, self.predicted_heading, self.accuracy)

    def get_global_position(self):
        x, y, heading, accuracy = self.get_local_position()

        lat = self.ref_lat + (y / RADIUS_EARTH) * (180.0 / math.pi)
        lon = self.ref_lon + (x / RADIUS_EARTH) * (180.0 / math.pi) / math.cos(self.ref_lat * math.pi / 180.0)

        gps_accuracy = 0.1 # 10 cm precision
        return (lat, lon, -heading + math.pi/2, gps_accuracy) # Lat, Lon, Heading to North

    def set_led(self, led_id, led_state):
        self.leds[led_id] = led_state


class AliceBot(object):
    def __init__(self, visualisation, sensors=None):
        if sensors is None:
            sensors = [Sensor(0.12, 0.08, 2, math.radians(30), math.radians(45)),
                       Sensor(0.14, 0.04, 2, math.radians(30), math.radians(15)),
                       Sensor(0.14, -0.04, 2, math.radians(30), math.radians(-15)),
                       Sensor(0.12, -0.08, 2, math.radians(30), math.radians(-45))]  # ,
        # Sensor(-0.15, 0, 2, math.radians(30), math.radians(-180))]

        # FIXME Delete these if program still runs correctly.
        #initial_action = [0.2, 0]
        #self.actions = [(0.2, -2), (0.2, 0), (0.2, 2)]
        #self.action_dimension = 2

        self.state_size = len(sensors)

        self.visualisation = visualisation

        x = 1
        y = 1
        heading = 0
        self.environment = simulator.Simulator()
        self.robot = Robot(x, y, heading, sensors, leds=[False, False])
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

        # Calculate true motion (with bias)
        v_left = BIAS_RIGHT * max(-MAX_SPEED_LEFT, min(MAX_SPEED_LEFT, action[0]))
        v_right = BIAS_LEFT * max(-MAX_SPEED_RIGHT, min(MAX_SPEED_RIGHT, action[1]))

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

        # Calculate predicted motion
        v_left = max(-MAX_SPEED_LEFT, min(MAX_SPEED_LEFT, action[0]))
        v_right = max(-MAX_SPEED_RIGHT, min(MAX_SPEED_RIGHT, action[1]))

        v_avg = 1.0 / 2.0 * (v_left + v_right)
        dx = math.cos(self.robot.heading) * v_avg
        dy = math.sin(self.robot.heading) * v_avg
        dtheta = 1.0 / self.wheel_distance * (v_right - v_left)

        self.robot.predicted_x += dx * dt
        self.robot.predicted_y += dy * dt
        self.robot.predicted_heading += dtheta * dt

        while self.robot.predicted_heading > math.pi:
            self.robot.predicted_heading -= 2 * math.pi
        while self.robot.predicted_heading <= -math.pi:
            self.robot.predicted_heading += 2 * math.pi

        self.visualisation.broadcast(self)

        return action, self.environment.reward(self.robot, self.size, -100, 1)


class EveBot(AliceBot):
    def __init__(self, visualisation):
        super(EveBot, self).__init__(visualisation, [Sensor(0.15, 0, 2, math.radians(30), 0)])
