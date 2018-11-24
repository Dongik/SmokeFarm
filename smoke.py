import socket
import numpy as np
import cv2
import imutils
import os
import signal
import subprocess as sp
import threading
from multiprocessing import Process, Queue


def read_bytes(socket, length):
    out = socket.recv(length)
    length -= len(out)
    while length > 0:
        more = socket.recv(length)
        out += more
        length -= len(more)
    return bytearray(out)


def read_frames(socket):
    version = read_bytes(socket, 1)[0]
    print("Version {}".format(version))
    banner_length = read_bytes(socket, 1)[0]
    banner_rest = read_bytes(socket, banner_length - 2)
    print("Banner length {}".format(banner_length))

    while True:
        frame_bytes = list(read_bytes(socket, 4))

        total = 0
        frame_bytes.reverse()
        for byte in frame_bytes:
            total = (total << 8) + byte

        print("JPEG data: {}".format(total))
        jpeg_data = read_bytes(socket, total)
        yield jpeg_data


def read_frame(socket):
    version = read_bytes(socket, 1)[0]
    print("Version {}".format(version))
    banner_lenth = read_bytes(socket, 1)[0]
    banner_rest = read_bytes(socket, banner_lenth - 2)
    print("Banner length {}".format(banner_lenth))

    frame_bytes = list(read_bytes(socket, 4))
    total = 0
    frame_bytes.reverse()
    for byte in frame_bytes:
        total = (total << 8) + byte

    print("JPEG data: {}".format(total))
    jpeg_data = read_bytes(socket, total)
    return jpeg_data



class Smoker:
    def __init__(self, config):
        self.devices = config["devices"]
    # def add_scenario(self):

    def start(self):
        print("start test")
        for device in self.devices:
            device.p_minicap = sp.Popen(["source", "minicap/run2.sh", "-s", device["id"]])

    def stop(self):
        print("stop test")
        for device in self.devices:
            os.killpg(os.getpgid(device.p_minicap.pid), signal.SIGTERM)


class Device:

    def __init__(self, device_id, number, port: int):
        self.device_id = device_id
        self.number = number
        self.__is_activated = False
        # adb forward tcp:1717 localabstract:minicap
        sp.call(["adb", "-s", device_id, "forward", "tcp:" + port, "localadstract:minicap"])
        self.connection = socket.create_connection(('127.0.0.1', port))
        # It should start screen

    def activate(self):
        print("start minicap")
        self.p_minicap = sp.Popen(["source", "minicap/run2.sh", "-s", self.device_id])

        print("open opencv window")
        self.connection = socket.create_connection(('127.0.0.1', 1717))

        for frame in read_frames(self.connection):
            img = np.array(bytearray(frame))
            img = cv2.imdecode(img, 1)
            img = cv2.resize(img, (540, 1110))
            cv2.imshow('capture', img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                exit(0)

        self.__is_activated = True

    def deactivate(self):
        print("canceling test")
        os.killpg(os.getpgid(self.p_minicap.pid), signal.SIGTERM)

        print("close opencv window")


    def adb(self, part):
        sp.call(["adb", "-s", self.device_id].extend(part))

    def adb_shell(self, part):
        sp.call(["adb", "-s", self.device_id, "shell"].extend(part))

    def touch(self, x, y):
        self.adb_shell([x, y])

    def touch_image(self, template_name, image_o):
        template = cv2.imread("templates/" + template_name + '.png')
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(image_o, cv2.COLOR_BGR2GRAY)

        loc = False
        threshold = 0.9
        w, h = template.shape[::-1]
        for scale in np.linspae(0.2, 1.0, 20)[::-1]:
            resized = imutils.resize(template, width=int(template.shape[1] * scale))
            w, h = resized.shape[::-1]
            res = cv2.matchTemplate(image, resized, cv2.TM_CCOEFF_NORMED)

            loc = np.where(res >= threshold)
            if len(zip(*loc[::-1])) > 0:
                break

        if loc and len(zip(*loc[::-1])) > 0:
            for pt in zip(*loc[::-1]):
                cv2.rectangle(image_o)
