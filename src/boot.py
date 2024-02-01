from odroid_go import GO
from machine import UART
from ui import draw_screen, draw_progress_bar
from time import time, sleep
import random

RX_PIN = 15
TX_PIN = 4

uart = UART(1, 9200, tx=TX_PIN, rx=RX_PIN, timeout=500)
SCREEN_WIDTH, SCREEN_HEIGHT = GO.lcd.winsize()

last_pump_was_running = False
last_pump_start_time = time()
last_pump_stop_time = time()

demo_mode = False


def handle_input():
    if GO.btn_start.was_pressed():
        global demo_mode
        demo_mode = not demo_mode


GO.lcd.clear()
while True:
    GO.update()
    handle_input()
    try:
        data = uart.readline().decode("utf-8")
        fields = data.strip().split(",")
        assert len(fields) == 7
    except Exception as e:
        if demo_mode:
            draw_screen(
                random.randint(0, 120),
                random.randint(0, 150),
                bool(random.randint(0, 1)),
                bool(random.randint(0, 1)),
                random.randint(0, 100),
            )
            sleep(0.1)
        else:
            draw_progress_bar(2, 100)
        continue

    firmare_version = fields[0]
    boiler_temp = int(fields[1])
    hx_temp = int(fields[3])
    countdown = int(fields[4])
    is_heating = bool(int(fields[5]))
    pump_running = bool(int(fields[6]))

    current_time = time()
    if pump_running and not last_pump_was_running:
        last_pump_start_time = current_time
        last_pump_was_running = True
    elif not pump_running and last_pump_was_running:
        last_pump_stop_time = current_time
        last_pump_was_running = False

    if pump_running:
        timer_value = current_time - last_pump_start_time
    else:
        timer_value = last_pump_stop_time - last_pump_start_time

    draw_screen(hx_temp, boiler_temp, is_heating, pump_running, timer_value)
