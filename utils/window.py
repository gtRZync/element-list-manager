import customtkinter as ctk
from utils.vector2 import Vector2

class Window(ctk.CTk):
    def __init__(self, title:str, size:Vector2[float]):
        self.mode_color =("#FFFFFF", "#323232")
        super().__init__(fg_color=self.mode_color)
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        self.__wm_center_window(size)
        self.title(title)
        self._size = size
        
    def get_size(self):
        return self._size
    
    def get_mode(self):
        return self._get_appearance_mode()
    
    def set_resizable(self, resizable: bool):
        self.resizable(resizable, resizable)

    def __wm_center_window(self, size: Vector2[float]):
        scale = self._get_window_scaling()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(((screen_width - size.x) // 2) * scale)
        center_y = int(((screen_height - size.y) // 2) * scale)
        geometry = f"{size.x}x{size.y}+{center_x}+{center_y}"
        self.geometry(geometry)