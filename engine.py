import os
import time
from threading import Thread

from datetime import date, datetime

from jardim.stylish import stylish_p, Style, Color

from utils import Style as MBStyle, Icon, save_json, get_json, is_active, get_foreground_exe, show_message_box

DATA_PATH = "data.json"
BACKUP_PATH = "backups\\{date}.json"
TICK_PERIOD = 0.1   # seconds
SAVE_PERIOD = 10    # seconds
BACKUP_PERIOD = 2   # hours


def save_loop(data):
    while True:
        try:
            save_json(DATA_PATH, data)
            stylish_p(
                f"{datetime.now().strftime('%H:%M:%S')} - Data saved",
                style=Style.BOLD,
                foreground=Color.GREEN
            )
        except Exception as e:
            stylish_p(
                f"Failed to save data:\n{e}",
                style=Style.BOLD,
                foreground=Color.RED
            )
        time.sleep(SAVE_PERIOD)


def backup_loop(data):
    while True:
        try:
            now = datetime.now()
            save_json(
                BACKUP_PATH.format(date=now.strftime("%Y-%m-%d - %H.%M.%S")),
                data
            )
            stylish_p(
                f"{now.strftime('%H:%M:%S')} - Data backed up",
                style=Style.BOLD,
                foreground=Color.PINK
            )
        except Exception as e:
            stylish_p(
                f"Failed to backup data:\n{e}",
                style=Style.BOLD,
                foreground=Color.RED
            )
        time.sleep(BACKUP_PERIOD * 60 * 60)


def init():
    # create JSON file if it doesn't exist
    if not os.path.exists(DATA_PATH):
        stylish_p(
            "Creating JSON file",
            style=Style.BOLD,
            foreground=Color.BLUE
        )
        save_json(DATA_PATH, {})


def run_loop(data):
    # save startup time
    last_tick = time.time()
    while True:
        tick = time.time()

        if is_active():
            today = date.today().strftime("%d/%m/%Y")

            # ------ TOTAL ------ #
            if today not in data:
                data[today] = {
                    "total": 0,
                    "apps": {}
                }
            data[today]["total"] += tick - last_tick

            # ----- PROCESS ----- #
            p_exe = get_foreground_exe()
            if p_exe is None:
                p_exe = "null"
            if p_exe not in data[today]["apps"]:
                data[today]["apps"][p_exe] = 0
            data[today]["apps"][p_exe] += tick - last_tick

        last_tick = tick
        time.sleep(TICK_PERIOD)


def main():
    try:
        init()

        # load data
        data = get_json(DATA_PATH)

        # FIXME: data is shared between threads without synchronization

        # create a thread to save data
        t1 = Thread(target=save_loop, args=(data,), daemon=True)
        t1.start()

        # create a thread to backup data
        t2 = Thread(target=backup_loop, args=(data,), daemon=True)
        t2.start()

        run_loop(data)
    except Exception as ex:
        show_message_box(
            "UsageStats - Fatal Error",
            f"An error occurred while running the engine:\n{ex}",
            MBStyle.OK,
            Icon.ERROR
        )
        exit(1)


if __name__ == "__main__":
    main()
