import smoke
import time

info = [
    {"device_id": "ec123123", "number": "+491732390496"},
    {"device_id": "ece21312", "number": "+412341234234"},
    {"device_id": "ecf32234", "number": "+492341234234"}
]




def precall(devices):
    dut0 = devices[0]
    dut1 = devices[1]

    dut0.start_call_app()
    dut0.type_text(dut1.number)

    dut0.touch_image("call+")

    # select comment
    dut0.touch_text("comment")
    dut0.type_text("Good")
    dut0.touch_text("DONE")

    # select map
    dut0.touch_text("map")
    dut0.wait_text("wait")
    dut0.touch_text("DONE")

    # select picture
    dut0.touch_text("picture")
    dut0.touch_image("sample")
    dut0.touch_text("DONE")

    # call
    dut0.touch_image("call")

    # check result
    dut0.wait_image("sample")
    dut0.wait_image("map")
    dut0.wait_text("Good")


def incall(devices):
    dut0 = devices[0]
    dut1 = devices[1]

    dut0.call(dut1.number)
    dut1.wait_text("Incoming")
    dut1.accept_call()

    # Shared Sketch
    dut1.touch_text("Share")
    dut1.touch_text("Sketch")
    dut0.touch_text("OK")

    # Shared Map
    dut0.touch_text_appear("Share")
    dut0.touch_text_appear("Map")
    dut0.touch_text_appear("OK")


def postcall(devices):
    dut0 = devices[0]
    dut1 = devices[1]

    dut0.call(dut1.number)
    time.sleep(2)
    dut0.end_call()
    dut0.touch_text("more")
    dut0.type_text("Hello")
    dut0.touch_text("DONE")
    dut1.wait_text_appear("Hello")

def one_to_one_chat(devices):
    dut0 = devices[0]
    dut1 = devices[1]

    dut0.start_messenger()
    dut0.type_text(dut1.number)
    dut0.touch_image("chat")
    time.sleep(1)

    dut0.touch_text("Hello")
    dut0.touch_image("send")

    dut1.touch_text("Hi")
    dut1.touch_image("send")

    # Attach many files
    dut0.touch_image("attach")
    dut0.swipe_up()
    dut0.touch_images("sample")
    dut0.swipe_down()
    dut0.touch_image("send")

    time.sleep(10)

    dut0.enable_wifi()

    dut1.detect_sequance_on_log(["good"])

    dut0.disable_wifi()

    dut0.touch_image("attach")
    dut0.swipe_up()
    dut0.touch_image("big")
    dut0.swipt_down()
    dut0.touch_image("send")

    dut0.enable_wifi()

    dut1.detect_sequance_on_log(["good"])


def group_chat(devices):
    dut0 = devices[0]
    dut1 = devices[1]
    dut2 = devices[2]

    dut0.start_messenger()

    dut0.type_text(dut1.number)
    dut0.touch_image("add")

    dut0.type_text(dut2.number)
    dut0.touch_image("add")

    dut0.touch_text("start")

    greeting = "Hello!Guys!"
    dut0.type_text(greeting)
    dut0.touch_image("send")

    dut1.touch_text(greeting)
    dut2.touch_text(greeting)


def chatbot(devices):
    dut0 = devices[0]

    dut0.start_messenger()
    dut0.touch_image("chat")
    dut0.type_text("+214334123")
    dut0.touch_text("enter")
    dut0.type_text("0-00")
    dut0.touch_text("bot")


devices = []
dut = smoke.Device("ce0917192db0a425057e", +821093733475, 1717)
dut.activate()
print("good")
dut.touch_text("Auto")
# for i in range(len(info)):
#     devices[i] = smoke.Device(info[i]["device_id"], info[i]["number"], 1717 + i)

# for i in range(len(info)):
#     devices[i].activate()

# precall(devices)
# incall(devices)
# postcall(devices)
# one_to_one_chat(devices)
# group_chat(devices)
# chatbot(devices)
