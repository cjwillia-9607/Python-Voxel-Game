import dearpygui.dearpygui as dpg

class Console:
    def __init__(self, app):
        self.app = app

    def run(self):
        dpg.create_context()
        dpg.create_viewport()
        dpg.set_viewport_title(title="Voxel Game GUI")
        dpg.setup_dearpygui()
        dpg.set_viewport_height(500)
        dpg.set_viewport_width(500)
        with dpg.window(label="Master Console", width=500, height=500):
            dpg.add_text("This is the master console, please close to resume game")
            dpg.add_button(label="Reset World", callback=self.reset_scene, width=300, height=30)
            with dpg.popup(dpg.last_item()):
                dpg.add_text("Resets the world and re-renders the scene")
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
    
    def reset_scene(self):
        self.app.reset_scene()
