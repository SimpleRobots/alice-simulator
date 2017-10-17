from time import sleep
import socket
import threading
import multiprocessing
import sys
from robot import AliceBot
from visualisation import VisualisationProvider, NetworkRenderer


HOST = "0.0.0.0"
PORT = 2323
POLL_RATE_HZ = 10

class Connection(object):
    def __init__(self, socket, parent):
        self.is_ai = False
        self.is_human = False
        self.sock = socket
        self.fsock = socket.makefile()
        self.parent = parent
        t = threading.Thread(target=self.receive)
        t.daemon = True
        t.start()

    def receive(self):
        while True:
            try:
                raw_cmd = self.fsock.readline().replace("\n", "")
                parts = raw_cmd.split(" ")
                cmd = parts[0]
                if cmd == "human":
                    print("Human registered")
                    self.is_human = True
                if cmd == "ai":
                    print("AI registered")
                    if not self.is_ai:
                        self.parent.ai_count += 1
                    self.is_ai = True
                if cmd == "drive" and self.is_human:
                    if self.parent.ai_mode:
                        print("Human stealing control")
                    self.parent.ai_mode = False
                    self.parent.set_speed(int(parts[1]), int(parts[2]))
                    self.parent.send_all_ais(raw_cmd)
                if cmd == "drive" and self.is_ai and self.parent.ai_mode:
                    self.parent.set_speed(int(parts[1]), int(parts[2]))
                    self.parent.send_all_ais(raw_cmd)
                if cmd == "reward":
                    print(raw_cmd)
                    self.parent.send_all_ais(raw_cmd)
                if cmd == "ai_mode" and self.is_human:
                    print("Handing over to ai")
                    self.parent.ai_mode = True
                if cmd == "led":
                    led_id = int(parts[1])
                    led_state = parts[2] == "True"
                    self.parent.alice.robot.set_led(led_id, led_state)
            except:
                break

    def send(self, msg):
        try:
            self.sock.send((msg + "\n").encode("utf-8"))
        except:
            print("Human disconnected")
            self.parent.disconnected(self)

    def send_to_human(self, msg):
        if self.is_human:
            try:
                self.sock.send((msg + "\n").encode("utf-8"))
            except:
                print("Human disconnected")
                self.parent.disconnected(self)

    def send_to_ai(self, msg):
        if self.is_ai:
            try:
                self.sock.send((msg + "\n").encode("utf-8"))
            except:
                print("AI disconnected")
                self.parent.disconnected(self)


class HardwareNetworkAPI(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.alice = AliceBot(VisualisationProvider())
        self.ai_mode = True
        self.ai_count = 0
        self.connections = []
        self.mark_for_removal = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST, PORT))
        self.sock.listen(10)
        self.action = [0, 0]
        t = threading.Thread(target=self.accept_connection)
        t.daemon = True
        t.start()

    def set_speed(self, v_l, v_r):
        self.action = [v_l / 100.0, v_r / 100.0]

    def sensor_loop(self):
        while True:
            if self.ai_count == 0:
                sleep(1)
            action, reward = self.alice.act(self.action, 1.0 / POLL_RATE_HZ)
            measurement = self.alice.get_measurements()
            self.send_all("sense " + " ".join(('%.2f' % x) for x in measurement))
            local_pos = self.alice.robot.get_local_position()
            global_pos = self.alice.robot.get_global_position()
            self.send_all("gps %.7f %.7f 0 %.3f 0 %.3f 0" % global_pos)
            self.send_all("pos %.3f %.3f %.3f %.3f" % local_pos)
            if reward < 0:
                self.alice.reset()
                self.send_all_ais("reward {}".format(reward))
            sleep( 1.0 / POLL_RATE_HZ )

    def accept_connection(self):
        while True:
            (clientsocket, address) = self.sock.accept()
            self.connections.append(Connection(clientsocket, self))
            print("Client connected")
            sys.stdout.flush()

    def disconnected(self, conn):
        self.mark_for_removal.append(conn)
        if conn.is_ai:
            self.ai_count -= 1

    def send_all(self, msg):
        self.lock.acquire()
        for x in self.connections:
            x.send(msg)
        for x in self.mark_for_removal:
            self.connections.remove(x)
        self.mark_for_removal = []
        self.lock.release()

    def send_all_ais(self, msg):
        self.lock.acquire()
        for x in self.connections:
            x.send_to_ai(msg)
        for x in self.mark_for_removal:
            self.connections.remove(x)
        self.mark_for_removal = []
        self.lock.release()

    def send_all_humans(self, msg):
        self.lock.acquire()
        for x in self.connections:
            x.send_to_human(msg)
        for x in self.mark_for_removal:
            self.connections.remove(x)
        self.mark_for_removal = []
        self.lock.release()


def visualisation():
    visualisation = NetworkRenderer("localhost")


def main():
    api = HardwareNetworkAPI()
    t = None
    if len(sys.argv) > 1 and (sys.argv[1] == "no-visualisation" or sys.argv[1] == "no-visualization"):
        print("Visualization disabled.")
    else:
        t = multiprocessing.Process(target=visualisation)
        t.start()
    try:
        api.sensor_loop()
    except:
        print("Stopping...")
    if t is not None:
        t.terminate()

if __name__ == "__main__":
    main()
