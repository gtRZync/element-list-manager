from utils import SideBar, ListBox, TypingPlaceholderEntry, ASSETS_DIR, DATA_DIR, Window, Vector2
from CTkListbox import * # type: ignore
from CTkMessagebox import * # type: ignore
import customtkinter as ctk
from pathlib import Path
from PIL import Image
import tkinter as tk
import threading
import time

WINDOW_WIDTH:int = 800
WINDOW_HEIGHT:int = 600
    
def center_window(win: ctk.CTkToplevel, size: Vector2[float]):
    """
    Do not call this method on a `Window` instance, it's already being done internally ight bromoto 🦧
    """
    scale = win._get_window_scaling() #type: ignore
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    center_x = int(((screen_width - size.x) // 2) * scale)
    center_y = int(((screen_height - size.y) // 2) * scale)
    geometry = f"{size.x}x{size.y}+{center_x}+{center_y}"
    win.geometry(geometry)
    
def save_element_to_file(window: ctk.CTk, listbox: ListBox, default_filename:str ):
    mode:str = window.get_mode() #type: ignore
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
    def save_elements(filepath: Path):
        elements: list = []
        size = listbox.size()
        try:
            for i in range(size):
                elements.append(listbox.get(i))
            with open(filepath, 'w') as file: #TODO: add extension check vro
                for element in elements:
                    file.write(f'{element}\n')
            listbox.set_was_saved(True)
            CTkMessagebox(window, title="Success", message=f"List successfully saved as {filepath.name}", fade_in_duration=1, button_color=btn_color, button_hover_color=btn_hover_color, button_text_color=btn_text_color)
        except FileNotFoundError as e:
            CTkMessagebox(window, title="File not found", message="Please select a valid file path", icon="warning", sound=True, button_color=btn_color, button_hover_color=btn_hover_color, button_text_color=btn_text_color)
            return
        except PermissionError as e:
            msg = e.strerror if e.strerror is not None else "A permission error has occured"
            CTkMessagebox(window, title="Permission error", message=msg, icon="warning", sound=True, button_color=btn_color, button_hover_color=btn_hover_color, button_text_color=btn_text_color)
            return
        
    def browse_files():
        pathvar = ctk.StringVar(value="None")
        path = ctk.filedialog.asksaveasfilename(parent=window, title="Save List", initialfile=f"{default_filename}", initialdir=DATA_DIR,defaultextension=".txt", filetypes=[('Text file', '*.txt *.dat')])
        if path:
            pathvar.set(path)
        return pathvar
    
    if listbox.size() == 0:
        CTkMessagebox(window, title="Save File Warning", message="Please add some elements before trying to save", icon="warning", sound=True, button_color=btn_color, button_hover_color=btn_hover_color, button_text_color=btn_text_color)
        return
    selected_path = browse_files()
    if selected_path.get().lower() == "none": return
    save_elements(Path(selected_path.get()))

def load_element_from_file(window: ctk.CTk, listbox: ListBox):
    selected_path = ctk.StringVar(value="No selected file")
    global win
    global filename
    mode:str = window.get_mode() #type: ignore
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
    if win and win.winfo_exists():
        return
    else:
        win = ctk.CTkToplevel(window)
        win.title("Load List")
        center_window(win, Vector2(400, 150))
        win.resizable(False, False)
        window.attributes('-disabled', True)
        win.attributes('-toolwindow', True)
        win.attributes('-topmost', True)
        label = ctk.CTkLabel(win, text="Select a file to load", font=ctk.CTkFont(family="JetBrains mono", size=15))
        label.pack()
        entry = ctk.CTkEntry(win, corner_radius=4, textvariable=selected_path, state=tk.DISABLED)
        entry.pack(expand=True, fill=tk.X, padx=20, pady=5)
        browse_btn = ctk.CTkButton(win, corner_radius=4, text="Browse Files", command=lambda: browse_files(selected_path))
        browse_btn.pack(padx=20, pady=10, side=tk.LEFT)
        submit_btn = ctk.CTkButton(win, corner_radius=4, text="Load elements", command= lambda: load_elements())
        submit_btn.pack(padx=5, pady=10, side=tk.LEFT)
        
    def load_elements():
        elements: list[str] = []
        initial_size = listbox.size()
        try:
            filename.set(Path(selected_path.get()).name)
            with open(selected_path.get(), 'r') as file:
                lines = file.readlines()
                for line in lines:
                    elements.append(line.strip("\n"))
            for element in elements:
                listbox.add_to_list(ctk.StringVar(value=element))
            win.destroy() #type: ignore
            if initial_size == 0:
                listbox.set_was_saved(True)
            CTkMessagebox(window, title="Success", message="Elements loaded successfully", fade_in_duration=1 ,button_color=btn_color, button_hover_color=btn_hover_color, button_text_color=btn_text_color)
        except FileNotFoundError as e:
            CTkMessagebox(win, title="File not found", message="Please select a valid file path", icon="warning", sound=True, button_color=btn_color, button_hover_color=btn_hover_color, button_text_color=btn_text_color)
            return
        except PermissionError as e:
            msg = e.strerror if e.strerror is not None else "A permission error has occured"
            CTkMessagebox(win, title="Permission error", message=msg, icon="warning", sound=True, button_color=btn_color, button_hover_color=btn_hover_color, button_text_color=btn_text_color)
            return
        
    def browse_files(pathvar: ctk.StringVar):
        path = ctk.filedialog.askopenfilename(parent=win, initialdir=DATA_DIR,title="Select a file to load", filetypes=[('Text file', '*.txt *.dat')])
        if path:
            pathvar.set(path)
    
    def enable_window():
        if win.winfo_exists(): #type: ignore
            window.after(100, enable_window)
            return
        window.attributes('-disabled', False)
        window.attributes('-topmost', True)
        window.attributes('-topmost', False)
    window.after(100, enable_window)
    
def prompt_for_element_saving(window: Window, listbox: ListBox, default_filename):
    if listbox.size() == 0 or not listbox.modified_after_save():
        window.quit()
        return
    
    msg = "Would you like to save your list to a file?"
    choices = ['yes', 'no']
    mode:str = window.get_mode()
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
    message = CTkMessagebox(
        window, 
        title="Save Elements", 
        icon="question", 
        message=msg, 
        options=choices, 
        option_1= "1", 
        button_color=btn_color, 
        button_hover_color=btn_hover_color, 
        button_text_color=btn_text_color
        )
    message.focus_set()
    if message.get() == "yes":
        save_element_to_file(window, listbox, default_filename)
        time.sleep(1)
        window.quit()
    elif message.get() == "no":
        window.quit()
                
def update_text():
    global filename
    global name
    global old_filename
    global lock
    global footer
    with lock:
        if filename.get() != old_filename:
            name.configure(text=f"Filename: {filename.get()}")
            old_filename = filename.get()
    footer.configure(text=f"Total Elements: {listbox.size()}")
    window.after(100, update_text)  
        

def bind_key_to_entry(btn: ctk.CTkButton, entry:ctk.CTkEntry, key:str):
    
    def invoke_btn(event: tk.Event, btn: ctk.CTkButton):
        if event.widget is entry._entry: #type: ignore
            if event.keysym.lower() == key.lower():
                btn.invoke()
    entry.bind("<Key>", lambda event: invoke_btn(event, btn))
    
    
def bind_key_to_listbox(btn: ctk.CTkButton, listbox:ListBox, key:str):
    
    def key_event(event: tk.Event, btn: ctk.CTkButton):
        if event.widget is listbox:
            if event.keysym.lower() == key.lower():
                btn.invoke()
            if event.keysym.lower() == "up":
                focused = listbox.curselection()
                if type(focused) is tuple:
                        new_index = (focused[0] - 1) % listbox.end_num
                        listbox.activate(focused[0]) #well, if this is not a good coder work then ion know 😼
                        listbox.select(new_index)
                        listbox.see(new_index)
            if event.keysym.lower() == "down":
                focused = listbox.curselection()
                if type(focused) is tuple: #TODO: reselect after press when deleted 
                    listbox.activate(focused[0])
                    new_index = (focused[0] + 1) % listbox.end_num
                    listbox.select(new_index)
                    listbox.see(new_index)
    listbox.bind("<Key>", lambda event: key_event(event, btn))

def clear_focus(event: tk.Event):
    if event.widget is window:
        window.focus_set()
        
def entry_get_focus_on_key(event: tk.Event):
    if event.widget is window and window.focus_get() != listbox:
        entry.focus_set()
    else:
        if event.keysym.lower() == "escape":
            window.focus_set()
            listbox.deactivate("all")

        
if __name__ == "__main__":
    window = Window("List Management", Vector2(WINDOW_WIDTH, WINDOW_HEIGHT))
    window.set_resizable(False)
    # icon=tk.PhotoImage(file=ASSETS_DIR / 'favicon.png')
    # window.after(201, lambda: window.iconphoto(False, icon))
    window.iconbitmap(ASSETS_DIR / 'favicon.ico')
    window.protocol("WM_DELETE_WINDOW", lambda: prompt_for_element_saving(window, listbox, filename.get()))
    window.bind("<Key>", entry_get_focus_on_key)
    window.bind("<Button-1>", clear_focus)
    win:ctk.CTkToplevel | None = None
    lock = threading.Lock()
    window.after(100, update_text) 
    
    
    text_entered = ctk.StringVar()
    field_width = WINDOW_WIDTH * .6
    IMG_sidebar = ctk.CTkImage(light_image=Image.open(ASSETS_DIR / "Sidebar_L.png"), dark_image=Image.open(ASSETS_DIR / "Sidebar_D.png"), size=(26, 26))
    IMG_plus = ctk.CTkImage(light_image=Image.open(ASSETS_DIR / "Plus_L.png"), dark_image=Image.open(ASSETS_DIR / "Plus_D.png"), size=(26, 26))
    IMG_delete = ctk.CTkImage(light_image=Image.open(ASSETS_DIR / "Delete_L.png"), dark_image=Image.open(ASSETS_DIR / "Delete_D.png"), size=(26, 26))
    filename:ctk.StringVar = ctk.StringVar(window, "Untilted.txt")
    old_filename:str = filename.get()
    sidebar:SideBar = SideBar(window, filename)
    sidebar.set_save_command(lambda: save_element_to_file(window, listbox, filename.get()))
    sidebar.set_load_command(lambda: load_element_from_file(window, listbox))
    
    name = ctk.CTkButton(
        window, 
        width=175, 
        height=44, 
        border_color="#B2B2B2", 
        border_width=1, 
        font=ctk.CTkFont(family="Inter", size=16, weight="bold"),
        text_color=("#1E1E1E", "#F5F5F5"), 
        fg_color=("#F0F0F0", "#3F3F3F"), 
        hover_color=("#A7A7A7","#2C2C2C"),
        text=f"Filename: {filename.get()}", 
        corner_radius=8, 
        cursor="hand2", 
        image=IMG_sidebar, 
        compound="right", 
        command=sidebar.show
        )
    name.pack(padx=10, pady=10, anchor="nw")

    title = ctk.CTkLabel(window, text="ELEMENTS ", text_color="#1E1E1E",font=ctk.CTkFont(family="Inter", size=60, weight="bold"))
    title.pack()
    listbox = ListBox(window, width=int(field_width), heihgt=150, multiple_selection=True)
    listbox.pack(padx=20, pady=20)
    entry = TypingPlaceholderEntry(
        window, 
        width=int(field_width), 
        height=40, 
        corner_radius=9999, 
        fg_color=("#2C2C2C", "#FFFFFF"),
        textvariable=text_entered, 
        border_color="#D9D9D9",
        text_color=("#F3F3F3", "#1E1E1E"),
        font=ctk.CTkFont(family="Inter", weight="bold", size=15)
        )
    entry.pack(padx=5, pady=15)
    listbox.set_entry(entry)
    btns = ctk.CTkFrame(window, width=175, height=44, fg_color="transparent")
    btns.pack(padx=10, pady=10)
    add_btn = ctk.CTkButton(
        btns, 
        width=170, 
        height=42, 
        corner_radius=8, 
        text="Add to list", 
        fg_color=( "#2C2C2C", "#FFFFFF"), 
        hover_color=("#1E1E1E", "#A7A7A7"), 
        text_color=( "#F5F5F5", "#2C2C2C" ), 
        image=IMG_plus, 
        compound="left", 
        cursor="hand2",
        font=entry.cget("font"),
        command=lambda: listbox.add_to_list(text_entered)
        )
    add_btn.pack(padx=50, pady=5, side="left")
    rm_btn = ctk.CTkButton(
        btns, 
        width=170, 
        height=42, 
        corner_radius=8, 
        text="Remove from list", 
        fg_color=( "#2C2C2C", "#FFFFFF"), 
        hover_color=("#1E1E1E", "#A7A7A7"), 
        text_color=( "#F5F5F5", "#2C2C2C" ), 
        image=IMG_delete, 
        compound="left",
        cursor="hand2",
        font=entry.cget("font"),
        command=listbox.remove
        )
    rm_btn.pack(padx=50, pady=5, side="left")
    bind_key_to_entry(add_btn, entry, "return")
    bind_key_to_listbox(rm_btn, listbox, "delete")
    footer = ctk.CTkLabel(
        window, 
        text=f"Total Elements: 0", 
        font=ctk.CTkFont(family="Inter", size=15, weight="bold", underline=True),
        text_color=( "#1E1E1E", "#F5F5F5" )
        )
    footer.pack(side="bottom", anchor="e", padx=10, pady=5)

    window.mainloop()