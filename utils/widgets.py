import customtkinter as ctk
import tkinter as tk
from CTkListbox import * # type: ignore
from CTkMessagebox import * # type: ignore
from PIL import Image
import tkinter as tk
from pathlib import Path
from typing import Callable, Any, Tuple
import threading

ASSETS_DIR:Path = Path('assets/icons')
DATA_DIR:Path   = Path('data')


class ListBox(CTkListbox):
    def __init__(self, root, width: int = 140, heihgt:int = 100, multiple_selection: bool = False, placeholder_text: str | None = None):
        self.root = root
        self.width = width
        self.height = heihgt
        self.mode_color = ("#2C2C2C", "#FFFFFF")
        self.placeholder_text = placeholder_text
        self.__was_saved:bool = False
        self.__size_after_save:int = -1
        self.lock = threading.Lock()
        super().__init__(
            root, 
            width=width, 
            height=heihgt, 
            multiple_selection=multiple_selection, 
            fg_color=self.mode_color, #type: ignore
            border_width=2,
            text_color=("#F3F3F3", "#1E1E1E"),  # type: ignore
            #? highlight_color="cornflower blue", maybe?
            font=ctk.CTkFont(family="Inter", weight="normal", size=15)  # type: ignore
            )
        self.bind("<Button-1>", lambda event: self.focus_set())
        self.__schedule_save_check()
        
    def __schedule_save_check(self):
        if self.master.winfo_exists():
            self.master.after(100, self.__on_change)
            
    def add_to_list(self, item:ctk.StringVar):
        """
        Add a string element to a CTkListbox
        
        I just wanted to use a try-except block since i don't usually do 🦧
        but yeah you cannot add a bunch of space or empty element not even the placeholder message lol
        , i'm a pretty good developper hehe 😼
        
        Parameters
        ----------
            item (ctk.StringVar): A variable that stores a string and automatically updates associated widgets when the value changes.
        See Also
        --------
            remove: Delete selected elements from the current CTkListbox's object.
        """
        EMPTY = ""
        try:
            if item.get().strip() == EMPTY or self.placeholder_text and item.get().strip() == self.placeholder_text:
                if item.get() != self.placeholder_text:
                    item.set(EMPTY)
                raise AttributeError()
            self.insert(tk.END, item.get())
            item.set(EMPTY)
        except AttributeError:
            mode:str = self.root.get_mode()
            btn_color:str =  ""
            btn_hover_color:str =  ""
            btn_text_color:str =  ""
            if mode.lower() == "dark":
                btn_color =  "#FFFFFF"
                btn_hover_color =  "#A7A7A7"
                btn_text_color:str = "#2C2C2C"
            else:
                btn_color =  "#2C2C2C"
                btn_hover_color =  "#1E1E1E"
                btn_text_color:str = "#F5F5F5"
            CTkMessagebox(self.root, title="Element error", message="Element cannot be an empty entry!!", icon="warning", sound=True, button_color=btn_color, button_hover_color=btn_hover_color, button_text_color=btn_text_color) 
        
    def remove(self):
        """
        Delete selected elements from a CTkListbox.

        Brotato chips, this is a cool function to delete elements from a CTkListbox.
        It even takes into account that the indexes will change with each delete. I'm a dumb genius vro ✌🏻😭

        See Also
        --------
            add_to_list: add a string element to the current CTkListbox's object
        """
        try:
            focused = self.curselection()
            if type(focused) is int:
                self.delete(focused)
            elif type(focused) is tuple:
                if len(focused) == 0: 
                    return
                elif len(focused) == 1:
                    self.delete(focused[0])
                    return
                elif len(focused) == self.size():
                    self.delete(tk.ALL)
                    return
                idx = 0
                for element in focused:
                    self.delete(element - (1 * idx) )
                    idx += 1
            else:
                return
        except Exception as e: #! gotta do better brotosynthesis ✌🏻😭
            print(e)
            return
        
    def set_was_saved(self, saved: bool):
        with self.lock:
            self.__was_saved = saved
            self.__size_after_save = self.size()
        
    def __on_change(self):
        with self.lock:
            if self.__was_saved:
                if self.__size_after_save != self.size():
                    self.__was_saved = False
        self.__schedule_save_check()
        
    def modified_after_save(self):
        with self.lock:
            return not self.__was_saved
        
    def set_placeholder_text(self, placeholder_text: str):
        self.placeholder_text = placeholder_text

class SideBar(ctk.CTkFrame):
    def __init__(self, root: ctk.CTk, filename: ctk.StringVar):
        self.root = root
        self.filename = filename
        self.scale = root._get_window_scaling()
        self.width = self.__scale_down(root.winfo_width()) 
        self.height = self.__scale_down(root.winfo_height()) 
        self.prev_width = self.width
        self.prev_height = self.height
        self.name_label_prev_color:str = ""
        self.__mode_color:dict[str, tuple[str, str]] = {
            "btn_fg_color": ( "#2C2C2C", "#FFFFFF"),
            "btn_text_color": ( "#F5F5F5", "#2C2C2C" ),
            "btn_hover_color": ("#1E1E1E", "#A7A7A7"), 
            "sidebar" : ( "#DADADA", "#3F3F3F"),
            }
        super().__init__(root, width=self.width, height=self.height, fg_color=self.__mode_color.get("sidebar"))
        self.pack_propagate(False)
        self.IMG_SIDEBAR = ctk.CTkImage(
            light_image=Image.open(ASSETS_DIR / "Sidebar_L.png"),
            dark_image=Image.open(ASSETS_DIR / "Sidebar_D.png"),
            size=(26, 26)
            )
        self.IMG_LOAD = ctk.CTkImage(
            light_image=Image.open(ASSETS_DIR / "Loader_L.png"),
            dark_image=Image.open(ASSETS_DIR / "Loader_D.png") 
            )
        self.IMG_SAVE = ctk.CTkImage(
            light_image=Image.open(ASSETS_DIR / "Save_L.png"),
            dark_image=Image.open(ASSETS_DIR / "Save_D.png") 
            )
        self.icon_width = self.IMG_SIDEBAR.cget("size")[0] 
        self.icon = ctk.CTkButton(self, width=self.icon_width, image=self.IMG_SIDEBAR, text="", fg_color="transparent", hover_color=("#A7A7A7","#2C2C2C"), corner_radius=8, command=self.hide)
        self.icon.pack(padx=10, pady=10, anchor="ne")
        self.name_label = ctk.CTkEntry(self, 
                                       width=150, 
                                       height=20, 
                                       border_width=0, 
                                       border_color="cornflower blue",
                                       fg_color="transparent",
                                       textvariable=self.filename,
                                       justify="center",
                                       font=ctk.CTkFont(
                                           family="Inter", 
                                           weight="normal", 
                                           underline=True, 
                                           size=20
                                           )
                                       )
        self.name_label.pack( ipady=5, anchor="center")
        self.name_label.bind("<FocusIn>", lambda event: self.__name_label_focus_in())
        self.name_label.bind("<FocusOut>", lambda event: self.__name_label_focus_out())
        self.name_label.bind("<Enter>", lambda event: self.__name_label_hovered())
        self.name_label.bind("<Leave>", lambda event: self.__name_label_not_hovered())
        self.name_label.bind("<Key>", self.__name_label_confirm)
        self.options = ["system", "dark", "light"]
        self.mode = ctk.CTkOptionMenu(
            self, 
            width=158, 
            height=39, 
            values=self.options, 
            text_color=( "#F5F5F5", "#2C2C2C" ), 
            fg_color=("#2C2C2C", "#FFFFFF"), 
            button_color=("#FFFFFF", "#2C2C2C"), 
            button_hover_color=("#ADADAD", "#1E1E1E"), 
            font=ctk.CTkFont(family="Inter", weight="bold", size=15),
            command=self.__set_mode
            )
        self.mode.pack(padx=10, pady=10, side="bottom", anchor="sw")
        self.space = ctk.CTkFrame(self, height=self.height //5, fg_color="transparent")
        self.space.pack()
        self.save_btn = ctk.CTkButton(
            self, 
            width=170, 
            height=40, 
            corner_radius=8, 
            text="Save List", 
            fg_color=self.__mode_color.get("btn_fg_color"), 
            hover_color=self.__mode_color.get("btn_hover_color"), 
            text_color=self.__mode_color.get("btn_text_color"), 
            image=self.IMG_SAVE, 
            cursor="hand2",
            font=self.mode.cget("font")
            )
        self.save_btn.pack(padx=5, pady=14)
        self.load_btn = ctk.CTkButton(
            self, 
            width=170, 
            height=40, 
            corner_radius=8, 
            text="Load List", 
            fg_color=self.__mode_color.get("btn_fg_color"), 
            hover_color=self.__mode_color.get("btn_hover_color"), 
            text_color=self.__mode_color.get("btn_text_color"), 
            image=self.IMG_LOAD, 
            cursor="hand2",
            font=self.mode.cget("font")
            )
        self.load_btn.pack(padx=5, pady=14)
        self.root.bind("<Configure>", lambda event: self.__reconfigure(event))
        self.bind("<Button-1>", lambda event: self.focus())
        self.space.bind("<Button-1>", lambda event: self.space.focus())
        self.mode.bind("<Button-1>", lambda event: self.mode.focus())
        self.name_label._is_focused = False  #type: ignore
        
    def __scale_down(self, x: int | float):
        return int(x // self.scale)
    
    def __reconfigure(self, event: tk.Event):
        """
        Useless in this case, since i don't allow resizing. Yeaaaah very lazy of me right??...but ion care lol 😹😹
        """
        if event.widget is self.root:
            self.width = self.__scale_down(event.width) // 3
            self.height = self.__scale_down(event.height) 
            if self.prev_width != self.width or self.prev_height != self.height:
                self.configure(width=self.width, height=self.height)
                self.space.configure(width=self.width - 3 , height=self.height // 5)
                self.prev_width = self.width
                self.prev_height = self.height
    def __name_label_focus_in(self):
        width = self.width - 4
        self.name_label.configure(width=width, border_width=2)
        self.name_label.select_range(0, tk.END)
        self.name_label.cget('font').configure(underline=False)
        self.name_label.configure(fg_color=self.cget("fg_color"))
        
    def __check_filename(self):
        tmp:Path = Path(self.filename.get())
        if tmp.suffix == '':
            self.filename.set(tmp.with_suffix('.txt').name)
        
    def __name_label_focus_out(self):
        new_width = self.name_label.cget("font").measure(self.name_label.get())
        self.name_label.configure(width=max(new_width + 50, 150), border_width=0) #TODO: make it show elipsis if the text's too long
        self.name_label.cget('font').configure(underline=True)
        if self.filename.get().strip() == "":
            self.filename.set("Untilted.txt")
        self.__check_filename()
        
        
    def __name_label_hovered(self):
        if self.name_label._is_focused: # type: ignore
            self.name_label.configure(fg_color=self.cget("fg_color"))
        else:
            self.name_label.configure(fg_color=("#A7A7A7","#2C2C2C"))
            
        
    def __name_label_not_hovered(self):
        self.name_label.configure(fg_color=self.cget("fg_color"))
        
    def __name_label_confirm(self, event: tk.Event):
        if event.widget is self.name_label._entry: # type: ignore
            if event.keysym.lower() == "return":
                self.focus()
        
    def set_save_command(self, command: Callable[[], Any]):
        self.save_btn.configure(command=command)
        
    def set_load_command(self, command: Callable[[], Any]):
        self.load_btn.configure(command=command)
        
    def hide(self):
        self.place_forget()
            
    def show(self):
        """
        I'm not removing the button from the screen cuz i'm lazy,
        but it gets hidden by the sidebar lol 😹
        """
        self.place(x=0, y=0)
        self.lift()
            
    def __set_mode(self, mode):
        ctk.set_appearance_mode(mode)
        
class TypingPlaceholderEntry(ctk.CTkEntry):
    def __init__(
        self, 
        master: Any, 
        width: int = 140, 
        height: int = 28, 
        corner_radius: int | None = None, 
        border_width: int | None = None, 
        fg_color: str | Tuple[str, str] | None = None, 
        border_color: str | Tuple[str, str] | None = None, 
        text_color: str | Tuple[str, str] | None = None, 
        placeholder: str = "Enter some text...",
        textvariable: ctk.Variable | None = None, 
        font: tuple | ctk.CTkFont | None = None, 
        **kwargs
        ):
        super().__init__(
            master, 
            width, 
            height, 
            corner_radius, 
            border_width, 
            fg_color=fg_color, 
            border_color=border_color, 
            text_color=text_color,  
            textvariable=textvariable, 
            font=font, 
            **kwargs
            )
        self.placeholder = placeholder
        self.placeholder_color = "gray"
        self.default_fg_color = self._entry.cget("fg")
        self.saved_color = text_color
        


        self._entry.insert(0, self.placeholder)
        self._entry.configure(fg=self.placeholder_color)


        self._entry.bind("<Key>", self._on_type)
        self._entry.bind("<FocusOut>", self._on_focus_out)
        self._entry.bind("<FocusIn>", self._on_focus_in)
        self._entry.bind("<Button-1>", self._on_focus_in)
        
        self.user_typed = False

    def _on_type(self, event):
        if not self.user_typed:
            self._entry.delete(0, "end")
            if self._get_appearance_mode().lower() == "light":
                self._entry.configure(fg=self.saved_color[0] if self.saved_color else '#F3F3F3')
            else:
                self._entry.configure(fg=self.saved_color[1] if self.saved_color else '#1E1E1E')
                self._text_color = self.saved_color
            self.user_typed = True

    def _on_focus_out(self, event):
        if self._entry.get().strip() == "":
            self._entry.insert(0, self.placeholder)
            self._entry.configure(fg=self.placeholder_color)
            self._text_color = self.placeholder_color
            self.user_typed = False
            
    def _on_focus_in(self, event):
        if self._entry.get().strip() == "" or self._entry.get().strip() == self.placeholder:
            self._entry.icursor(0)