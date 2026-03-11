import os
import time


def animated_exit(delay_seconds: float, dots: int):
    print("kilépés", end=" ", flush=True)
    for _ in range(dots):
        print(".", end="", flush=True)
        time.sleep(delay_seconds)
    print("")


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")