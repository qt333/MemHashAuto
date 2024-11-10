import pyautogui
import time
import pygetwindow as pg
import random
from art import text2art
from colorama import init
from termcolor import colored
import ctypes
import random
import sys
from math import ceil

def script_info(name: str = "MemHashAuto"):
    init() 
    print(colored(text2art('MemHashAuto'), "green"))

    if sys.platform == 'win32':
        ctypes.windll.kernel32.SetConsoleTitleW(f"{name}")

    print(
        f"{colored('Github: https://github.com/qt333/', color='light_yellow')}\n"
        f"{colored('Donate (TON): UQD9bAZ5I8w2iqBJfNmv3Lpezm-2HfYMoDQVWQOo7AXodNyf', color='light_green')}"
    )

def get_window():
    """
    Get the blum window.

    :return: The blum window
    """
    windows = next(
        (
            pg.getWindowsWithTitle(opt)
            for opt in ["TelegramDesktop", "64Gram", "AyuGram", "telegram-desktop"]
            if pg.getWindowsWithTitle(opt)
        ),
        None,
    )

    window = windows[0] if windows else None

    if window and not window.isActive:
        # window.minimize()
        window.restore()

        return window
    elif window.isActive:
        return window

    return None

def get_rect(window):
        """
        Get the rectangle coordinates of the given window.

        :param window: The window object
        :return: A tuple containing the coordinates (left, top, width, height)
        """
        return (window.left, window.top, window.width, window.height)

def click_start_button(screen, rect):
    time.sleep(random.random())
    width, height = screen.size
    screen_x = rect[0] + ceil(width * 0.485)
    screen_y = rect[1] + ceil(height * 0.6502)
    pyautogui.click(
        screen_x + random.randint(1,10),
        screen_y + random.randint(1,10), button='LEFT'
    )

def detected_low_energy_status(screen, rect):
    width, height = screen.size
    screen_x = rect[0] + ceil(width * 0.4253)
    screen_y = rect[1] + ceil(height * 0.5056)
    R, G, B = pyautogui.pixel(screen_x, screen_y)
    red_range = (R > 220) and (90 <= G < 121) and (90 <= B < 113)
    return red_range

def detected_full_energy_status(screen, rect):
    width, height = screen.size
    full_energy_color = (175, 253, 181)
    screen_x = rect[0] + ceil(width * 0.5945)
    screen_y = rect[1] + ceil(height * 0.2289)
    R, G, B = pyautogui.pixel(screen_x, screen_y)
    if full_energy_color == (R, G, B):
        return True
    else:
        return False

def capture_screenshot(rect):
    """
    Capture a screenshot of the specified region.

    :param rect: A tuple containing the region coordinates (left, top, width, height)
    :return: A screenshot image of the specified region
    """
    return pyautogui.screenshot(region=rect)

def main():
    
    script_info()
    
    cycle = 0
    c = 0
    # button_start_coord = (195, 463)
    # energy_status_pixel_coord = (171, 360)
    # full_energy_pixel_coord = (239, 163)
    # full_energy_color = (175, 253, 181) #green
    window = get_window()
    if not window:
        print(f"{colored('Window not found!', color='red')}")
        return
    rect = get_rect(window)
    screenshot = capture_screenshot(rect)
    try:
        while True:
            time.sleep(2)
            window = get_window()
            # print(window)
            if window:
                rect = get_rect(window)
                # if detected_full_energy_status(screenshot, rect, full_energy_pixel_coord):
                if detected_full_energy_status(screenshot, rect):
                    print(f'Started | Starting mining №{c}')
                    # click_start_button(screenshot, rect, button_start_coord)
                    click_start_button(screenshot, rect)
                    # cycle += 1
                    c += 1
                # if detected_low_energy_status(screenshot, rect, energy_status_pixel_coord):
                if detected_low_energy_status(screenshot, rect):
                    # click_start_button(screenshot, rect, button_start_coord)
                    click_start_button(screenshot, rect)
                    print('Stopped | Waiting for energy restore...')
                    # cycle = 0

            time.sleep(20)
    except KeyboardInterrupt:
        print("Process interrupted. Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()