import threading
from voxelengine import VoxelEngine
from console import Console
import random

engine = None
reset = False
seed = random.randint(0, 1000000)
def run_game():
    global engine 
    engine = VoxelEngine(seed)
    engine.run()

def run_console():
    global engine
    half_report = True
    while engine is None:
        if half_report:
            print("Waiting for engine to initialize.")
        half_report = not half_report
        pass
    console = Console(engine)
    console.run()

if __name__ == "__main__":
    engine_thread = threading.Thread(target=run_game)
    console_thread = threading.Thread(target=run_console)

    engine_thread.start()
    console_thread.start()

    engine_thread.join()
    console_thread.join()
