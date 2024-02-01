from odroid_go import GO
import math
from time import sleep

SCREEN_WIDTH, SCREEN_HEIGHT = GO.lcd.winsize()


def draw_temperature_gauge(temperature, x, y, radius=80, thickness=15):
    start_angle_arc = 240
    end_angle_arc = 480

    min_temp = 20
    max_temp = 100
    scaling_factor = max_temp / (end_angle_arc - start_angle_arc)

    # Calculate the angle for the green zone of the gauge (90 degrees celcius to 100 degrees celcius)
    start_angle_green = int(start_angle_arc + (90 - min_temp) / scaling_factor)
    end_angle_green = int(start_angle_arc + (100 - min_temp) / scaling_factor)

    GO.lcd.arc(
        x,
        y,
        radius + 5,
        thickness // 2,
        start_angle_arc,
        start_angle_green,
        color=GO.lcd.BLUE,
        fillcolor=GO.lcd.BLUE,
    )
    GO.lcd.arc(
        x,
        y,
        radius + 5,
        thickness // 2,
        start_angle_green,
        end_angle_green,
        color=GO.lcd.GREEN,
        fillcolor=GO.lcd.GREEN,
    )
    GO.lcd.arc(
        x,
        y,
        radius + 5,
        thickness // 2,
        end_angle_green,
        end_angle_arc % 360,
        color=GO.lcd.RED,
        fillcolor=GO.lcd.RED,
    )

    # Draw the temperature as a inner arc of the gauge
    temperature_clamped = min(max(temperature, min_temp), max_temp)
    temperature_angle = int(
        start_angle_arc + (temperature_clamped - min_temp) / scaling_factor
    )

    temperature_color = GO.lcd.GREEN
    if temperature <= 90:
        temperature_color = GO.lcd.CYAN
    elif temperature >= 100:
        temperature_color = GO.lcd.RED

    GO.lcd.arc(
        x,
        y,
        radius - 10,
        thickness,
        start_angle_arc,
        temperature_angle,
        color=temperature_color,
        fillcolor=temperature_color,
    )

    GO.lcd.arc(
        x,
        y,
        radius - 10,
        thickness,
        temperature_angle,
        end_angle_arc % 360,
        color=GO.lcd.NAVY,
        fillcolor=GO.lcd.NAVY,
    )

    # Shift angles by 90 degrees so 0 degrees is at the top of the gauge
    start_angle_arc -= 90
    end_angle_arc -= 90

    # Draw temperature labels around the gauge
    step_size = int(10 / scaling_factor)
    for i in range(start_angle_arc, end_angle_arc + 1, step_size):
        angle = i % 360
        degrees = min_temp + int((i - start_angle_arc) * scaling_factor)
        label_x = math.cos(math.radians(angle)) * (radius + 20)
        label_x += x
        # shift text by length of text to center it
        label_x -= len(str(degrees)) * 3
        label_y = math.sin(math.radians(angle)) * (radius + 20)
        label_y += y
        # shift text by height of text to center it
        label_y -= 2
        GO.lcd.font(GO.lcd.FONT_Small)
        GO.lcd.text(int(label_x), int(label_y), str(degrees), color=GO.lcd.WHITE)

    # Clear the center of the gauge
    GO.lcd.circle(x, y, 50, color=GO.lcd.BLACK, fillcolor=GO.lcd.BLACK)

    # Draw temperature label
    GO.lcd.font(GO.lcd.FONT_DejaVu24)
    label_text = "{} C".format(temperature)
    GO.lcd.text(
        x - len(label_text) * 7,
        y - 10,
        label_text,
        color=GO.lcd.WHITE,
    )


def draw_steam_gauge(temperature, x, y, height, width):
    # Draw a bar plot of the temperature
    min_temp = 20
    max_temp = 150
    scaling_factor = (max_temp / height) if height > 0 else 1
    temperature_clamped = min(max(temperature, min_temp), max_temp)
    temperature_height = int((temperature_clamped - min_temp) / scaling_factor)
    GO.lcd.rect(
        x,
        y,
        width,
        height,
        color=GO.lcd.NAVY,
        fillcolor=GO.lcd.NAVY,
    )
    GO.lcd.rect(
        x,
        y + height - temperature_height,
        width,
        temperature_height,
        color=GO.lcd.CYAN,
        fillcolor=GO.lcd.CYAN,
    )

    # Clear the right side of the gauge
    GO.lcd.rect(
        x + width,
        y,
        50,
        height + 10,
        color=GO.lcd.BLACK,
        fillcolor=GO.lcd.BLACK,
    )

    # Draw a temperature label
    GO.lcd.font(GO.lcd.FONT_Small)
    GO.lcd.text(
        x + width + 10,
        y + height - temperature_height - 5,
        "{} C".format(temperature),
        color=GO.lcd.WHITE,
    )


def draw_heat_widget(state, x, y):
    if state:
        GO.lcd.image(x, y, "imgs/flame.bmp")
    else:
        # Clear the widget
        GO.lcd.rect(
            x,
            y,
            20,
            20,
            color=GO.lcd.BLACK,
            fillcolor=GO.lcd.BLACK,
        )


def draw_pump_widget(state, x, y):
    if state:
        GO.lcd.image(x, y, "imgs/water.bmp")
    else:
        # Clear the widget
        GO.lcd.rect(
            x,
            y,
            20,
            20,
            color=GO.lcd.BLACK,
            fillcolor=GO.lcd.BLACK,
        )


def draw_timer_widget(time, x, y):
    # Show a timer widget with the time in seconds and milliseconds lika a stopwatch, time is in seconds
    minutes = int(time // 60)
    seconds = int(time) % 60
    milliseconds = int((time - int(time)) * 1000)
    label_text = "{:02d}:{:02d}:{:03d}".format(minutes, seconds, milliseconds)

    # Clear the widget
    GO.lcd.rect(
        x - len(label_text) * 10,
        y,
        len(label_text) * 10,
        32,
        color=GO.lcd.BLACK,
        fillcolor=GO.lcd.BLACK,
    )

    GO.lcd.font(GO.lcd.FONT_7seg)
    GO.lcd.text(
        x - len(label_text) * 10,
        y,
        label_text,
        color=GO.lcd.WHITE,
    )


def draw_screen(hx_temp, boiler_temp, is_heating, pump_running, time_passed):
    padding = 10

    heat_widget_width = 20
    heat_widget_height = 20

    steam_widget_width = 20
    steam_widget_height = SCREEN_HEIGHT - padding * 3 - heat_widget_height

    draw_temperature_gauge(
        hx_temp,
        SCREEN_WIDTH // 2 + steam_widget_width + padding,
        SCREEN_HEIGHT // 2,
    )
    draw_steam_gauge(
        boiler_temp,
        padding,
        padding,
        steam_widget_height,
        steam_widget_width,
    )
    draw_heat_widget(is_heating, padding, steam_widget_height + padding * 2)
    draw_pump_widget(
        pump_running,
        heat_widget_width + padding * 2,
        steam_widget_height + padding * 2,
    )
    draw_timer_widget(
        time_passed,
        SCREEN_WIDTH // 2 + steam_widget_width + padding,
        SCREEN_HEIGHT - padding * 4,
    )


def draw_progress_bar(
    duration_seconds, steps, color=GO.lcd.GREEN, padding=50, height=20
):
    GO.lcd.clear()
    GO.lcd.font(GO.lcd.FONT_DejaVu24)
    GO.lcd.text(
        GO.lcd.CENTER,
        SCREEN_HEIGHT // 2,
        "Waiting for data...",
        color=GO.lcd.GREEN,
    )
    for i in range(1, steps + 1):
        GO.lcd.rect(
            padding,
            SCREEN_HEIGHT // 2 - 50,
            ((SCREEN_WIDTH - padding * 2) // steps) * i,
            height,
            color,
            fillcolor=color,
        )
        sleep(duration_seconds / steps)
    GO.lcd.clear()
