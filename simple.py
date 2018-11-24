import socket
import numpy as np
import cv2
import imutils

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

def touch(loc):
    return

def touch_image(template_name, image_o):
    template = cv2.imread(template_name + '.png')
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


connection = socket.create_connection(('127.0.0.1', 1717))

for frame in read_frames(connection):
    img = np.array(bytearray(frame))
    img = cv2.imdecode(img, 1)
    img = cv2.resize(img, (540, 1110))
    cv2.imshow('capture', img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        exit(0)
    pass
