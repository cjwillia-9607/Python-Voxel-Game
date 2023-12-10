import dearpygui.dearpygui as dpg
from settings import *

engine = None

class Console:
    def __init__(self, app):
        global engine
        engine = app
        self.app = app
        self.app.console = self

    def run(self):
        dpg.create_context()
        dpg.create_viewport()
        dpg.set_viewport_title(title="Voxel Game GUI")
        dpg.setup_dearpygui()
        dpg.set_viewport_height(500)
        dpg.set_viewport_width(500)
        with dpg.window(label="Master Console", width=500, height=500):
            dpg.add_text("This is the master console, please close to resume game")
            dpg.add_button(label="Reset World", callback=reset_scene, width=300, height=30)
            with dpg.popup(dpg.last_item()):
                dpg.add_text("Resets the world and re-renders the scene")
            # text input
            dpg.add_text("Seed:")
            dpg.add_input_text(label="Seed Input", tag="seed", default_value=str(engine.seed), width=300, height=30)
            dpg.add_button(label="Set Seed", callback=set_seed, width=300, height=30)
            dpg.add_button(label="Exit Game", callback=exit, width=300, height=30)

        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
    
    def exit(self):
        exit()

def reset_scene():
    print("Resetting")
    engine.reset = True

def exit():
    global engine
    print("Exiting")
    engine.running = False
    dpg.destroy_context()
    engine = None

def set_seed():
    global engine
    engine.seed = int(dpg.get_value("seed"))
