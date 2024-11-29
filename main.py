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
from loguru import logger

def logging_setup():
    format_info = "<green>{time:HH:mm:ss.SS}</green> | <blue>{level}</blue> | <level>{message}</level>"
    logger.remove()

    logger.add(sys.stdout, colorize=True, format=format_info, level="INFO")
    logger.add("memhash.log", rotation="50 MB", compression="zip", format=format_info, level="TRACE")
    # if config.USE_TG_BOT:
    #     logger.add(lambda msg: send_log_to_telegram(msg), format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO")

logging_setup()

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
    # full_energy_color = (175, 253, 181)
    screen_x = rect[0] + ceil(width * 0.5945)
    screen_y = rect[1] + ceil(height * 0.2289)
    R, G, B = pyautogui.pixel(screen_x, screen_y)
    # if full_energy_color == (R, G, B):
    energy_range = (130 <= R <= 220) and (150 <= G <= 255) and (150 <= B <= 255)
    if energy_range:
        return True
    else:
        return False

def detected_partial_energy_status(screen, rect, step):
    width, height = screen.size
    # full_energy_color = (175, 253, 181)
    # partial_energy_color = (159, 179, 241) #blue
    # partial_energy_color = (177, 183, 253) #blue
    #(140, 175, 229) blue3 
    screen_x = rect[0] + ceil(width * 0.5945) - step
    screen_y = rect[1] + ceil(height * 0.2289)
    R, G, B = pyautogui.pixel(screen_x, screen_y)
    # blue_range_0 = (150 <= R <= 180) and (170 <= G < 190) and (230 <= B <= 255)
    # blue_range_1 = (170 <= R <= 190) and (170 <= G < 220) and (200 <= B <= 235)
    energy_range = (130 <= R <= 220) and (150 <= G <= 255) and (150 <= B <= 255)
    # print(screen_x, screen_y, (R, G, B))
    if energy_range:
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
        logger.info(f"{colored('Window not found!', color='red')}")
        return
    logger.info(f"{colored(f'Window found {window.title}!', color='white')}")
    logger.info(f"{colored(f'Mining will start automatically in a few seconds!', color='white')}")
    rect = get_rect(window)
    screenshot = capture_screenshot(rect)
    try:
        time.sleep(3)
        #initial cycle
        while True:
            window = get_window()
            if window:
                rect = get_rect(window)
                # if detected_full_energy_status(screenshot, rect, full_energy_pixel_coord):
                #NOTE search for energy pixel at 1st cycle. All other cycles will be proceed with full energy bar!
                if not cycle and not detected_low_energy_status(screenshot, rect):
                    for step in range(0, 111, 2):
                        if detected_partial_energy_status(screenshot , rect, step):
                            click_start_button(screenshot, rect)
                            cycle += 1
                            logger.info(f'Started | Starting mining №{cycle}')
                            break
                        time.sleep(0.05)
                if detected_low_energy_status(screenshot, rect):
                    time.sleep(0.1)
                    click_start_button(screenshot, rect)
                    logger.info('Stopped | Waiting for energy restore...')
                    break #exit from initial cycle
            else:
                logger.info(f"{colored('Window not found!', color='red')}")
                return
            time.sleep(10)

        while True:
            window = get_window()
            if window:
                rect = get_rect(window)
                #start mining when energy bar is full
                if detected_full_energy_status(screenshot, rect):
                    cycle += 1
                    logger.info(f'Mining | Starting mining cycle №{cycle}')
                    time.sleep(random.uniform(1,3))
                    click_start_button(screenshot, rect)
                #stop mining when status low energy
                if detected_low_energy_status(screenshot, rect):
                    click_start_button(screenshot, rect)
                    logger.info('Stopped | Waiting for energy restore...')
            else:
                logger.info(f"{colored('Window not found!', color='red')}")
                return
            time.sleep(30)
            #printing every 5 minutes that script wait for enegry restore
            if not (c % 10):
                logger.info(f'Resting | Waiting for energy restore...')
            c += 1
    except KeyboardInterrupt:
        logger.info("Process interrupted. Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()