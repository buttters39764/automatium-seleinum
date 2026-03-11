import time


def animated_exit(delay_seconds: float, dots: int):
    # kívánt forma: kilépés ...
    print("kilépés", end=" ", flush=True)
    for _ in range(dots):
        print(".", end="", flush=True)
        time.sleep(delay_seconds)
    print("")