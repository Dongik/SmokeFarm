import socket
import numpy as np
import cv2
import imutils
import os
import signal
import subprocess as sp
import time
import asyncio
import threading
from multiprocessing import Process, Queue
# from queue import Queue
import pytesseract


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

        # print("JPEG data: {}".format(total))
        jpeg_data = read_bytes(socket, total)
        yield jpeg_data

# queue = []
lock = threading.Lock()
import queue
latest = False
class WindowThread(threading.Thread):
    def run(self):
        connection = socket.create_connection(('127.0.0.1', 1717))
        global latest
        for frame in read_frames(connection):
            img = np.array(bytearray(frame))
            img = cv2.imdecode(img, 1)
            # print("qqq")
            # queue.put(img)
            image = cv2.resize(img, (540, 1110))
            lock.acquire()
            latest = image
            lock.release()
            cv2.imshow("window", image)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                exit(0)
            pass

class DetectTextThread(threading.Thread):
    def run(self):
        for i in range(1000):
            lock.acquire()
            image = latest
            lock.release()
            string = pytesseract.image_to_string(image)
            print(string)



WindowThread().start()
time.sleep(1)
DetectTextThread().start()




def show_window(device_id, queue):
    connection = socket.create_connection(('127.0.0.1', 1717))
    print("Hello")
    for frame in read_frames(connection):
        img = np.array(bytearray(frame))
        img = cv2.imdecode(img, 1)
        # print("qqq")
        # queue.put(img)
        image = cv2.resize(img, (540, 1110))

        cv2.imshow(device_id, image)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit(0)
        pass

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


class Device:

    def __init__(self, device_id, number, port=1717):
        self.device_id = device_id
        self.number = number
        self.__is_activated = False
        self.port = port
        self.connection = False
        self.queue = Queue(2)
        # It should start screen

    def activate(self):
        print("start minicap")
        # adb forward tcp:1717 localabstract:minicap
        sp.call(["adb", "forward", "tcp:1717", "localabstract:minicap"])
        p = sp.Popen(["./run2.sh", self.device_id], cwd="minicap/")
        time.sleep(4)
        print("open opencv window")
        t1 = threading.Thread(target=show_window, args=(self.device_id, self.queue))
        t2 = threading.Thread(target=show_window, args=(self.device_id + "-2", self.queue))
        t2.start()
        t1.start()
        # p_window = Process(target=self.show_window, args=(self,))
        # self.window()

        self.__is_activated = True




    def deactivate(self):
        print("canceling test")
        os.killpg(os.getpgid(self.p_minicap.pid), signal.SIGTERM)

        print("close opencv window")

    def adb(self, part):
        return sp.check_output(["adb", "-s", self.device_id].extend(part))

    def adb_shell(self, part):
        return sp.check_output(["adb", "-s", self.device_id, "shell"].extend(part))

    def touch(self, x, y):
        self.adb_shell([x, y])

    def show_window(self):
        connection = socket.create_connection(('127.0.0.1', 1717))
        print("Hello")
        for frame in read_frames(connection):
            img = np.array(bytearray(frame))
            img = cv2.imdecode(img, 1)
            # self.queue.put(img)
            image = cv2.resize(img, (540, 1110))

            cv2.imshow(self.device_id, image)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                exit(0)
            pass

    def find_text(self, text, image):
        string = pytesseract.image_to_string(image)
        print(string)

    def touch_text(self, text):
        connection = socket.create_connection(('127.0.0.1', 1717))

        for i in range(100):
            print("Good")
            time.sleep(1)

        # for i in range(3):
        #     print("Yey " + str(i))
        #     frame = read_frame(connection)
        #     img = np.array(bytearray(frame))
        #     img = cv2.imdecode(img, 1)
        #     image = cv2.resize(img, (540, 1110))
        #     string = pytesseract.image_to_string(image)
        #     print(string)
        #     time.sleep(0.1)
        #
        #
        # for frame in read_frames(connection):
        #     img = np.array(bytearray(frame))
        #     img = cv2.imdecode(img, 1)
        #     # gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        #     # edges = cv2.Canny(img, 100, 200)
        #     # img_new = gray.fromarray(edges)
        #     st = False
        #     ed = False
        #     count = len(text)
        #
        #     image = cv2.resize(img, (540, 1110))
        #
        #     cv2.imshow(self.device_id, image)
        #     if cv2.waitKey(25) & 0xFF == ord('q'):
        #         cv2.destroyAllWindows()
        #         exit(0)
        #     pass
            # boxes = pytesseract.image_to_boxes(img)
            # string = pytesseract.image_to_string(img)
            # print(string)
            # for box in boxes:
            #     print(box)
                # if box == text[count]:
                #     count += 1
                #     if count == len(text):
                #         bo
                # else:
                #     count = 0



    def touch_image(self, template_name):
        for frame in read_frames(self.connection):
            img = np.array(bytearray(frame))
            img = cv2.imdecode(img, 1)
            img = cv2.resize(img, (540, 1110))
            cv2.imshow('capture', img)

            # # template matching scalable
            # template = cv2.imread("templates/" + template_name + '.png')
            # template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            # image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #
            # loc = False
            # threshold = 0.9
            # w, h = template.shape[::-1]
            # for scale in np.linspace(0.2, 1.0, 20)[::-1]:
            #     resized = imutils.resize(template, width=int(template.shape[1] * scale))
            #     w, h = resized.shape[::-1]
            #     res = cv2.matchTemplate(image, resized, cv2.TM_CCOEFF_NORMED)
            #     loc = np.where(res >= threshold)
            #     if len(zip(*loc[::-1])) > 0:
            #         break
            #
            # if loc and len(zip(*loc[::-1])) > 0:
            #     for pt in zip(*loc[::-1]):
            #         cv2.rectangle(img,)
