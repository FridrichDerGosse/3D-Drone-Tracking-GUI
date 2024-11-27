"""
main.py
26. November 2024

GUI entry point

Author:
Nilusink
"""
from concurrent.futures import ThreadPoolExecutor
from icecream import ic
from time import perf_counter
from gui import *


SERVER_ADDRESS: tuple[str, int] = ("127.0.0.1", 20_000)


def main() -> None:
    # debugging setup
    start = perf_counter()

    def time_since_start() -> str:
        """
        stylized time since game start
        gamestart being time since `mainloop` was called
        """
        t_ms = round(perf_counter() - start, 4)

        t1, t2 = str(t_ms).split(".")
        return f"{t1: >4}.{t2: <4} |> "

    ic.configureOutput(prefix=time_since_start)
    debugger.init("./tracking.log", write_debug=False, debug_level=DebugLevel.info)

    pool = ThreadPoolExecutor()

    v = Viewer([], pool)

    dc = DataClient(
        SERVER_ADDRESS,
        pool,
        v
    )

    dc.start()

    while True:
        v.step()


if __name__ == '__main__':
    main()
