
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, StringVar, ttk, filedialog, Label
from audio.recorder import AudioRecorder
from audio.effects import tremolo_effect, echo_effect, reverb_effect, distortion_effect, wah_wah_effect
from PIL import ImageTk, Image


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def toggle_recording(button: tk.Button):
    if recorder.is_recording:
        button.config(image=record_button_img)
        recorder.stop_recording()
        current_input_path.set(recorder.file_path)
    else:
        button.config(image=pause_button_img)
        recorder.start_recording()

def select_file():
    selected_file_path = filedialog.askopenfilename(title="Select file", filetypes=[("WAV files", ".wav")])

    if selected_file_path is not None:
        current_input_path.set(selected_file_path)

def apply_effect():
    effect = current_effect.get()
    path = current_input_path.get()

    if effect == 'Echo':
        delay = entry_1.get()
        delay_amplifier = entry_2.get()
        echo_effect(path, "echo", float(delay), float(delay_amplifier))
    elif effect == 'Reverb':
        delay = entry_1.get()
        decay = entry_2.get()
        reverb_effect(path, "reverb", float(delay), float(decay))
    elif effect == 'Distortion':
        gain = entry_1.get()
        threshold = entry_2.get()
        distortion_effect(path, "distortion", float(gain), float(threshold))
    elif effect == 'Tremolo':
        rate = entry_1.get()
        depth = entry_2.get()
        tremolo_effect(path, "tremolo", float(rate), float(depth))
    elif effect == 'WahWah':
        lfo = entry_1.get()
        min = entry_2.get()
        max = entry_3.get()
        bandwidth = entry_4.get()
        wah_wah_effect(path, "wah_wah", float(lfo), float(min), float(max), float(bandwidth))


window = Tk()

recorder = AudioRecorder(0)

window.geometry("1280x720")
window.configure(bg = "#1897DF")

canvas = Canvas(
    bg="#1897DF",
    height=720,
    width=1280,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x = 0, y = 0)

pause_button_img = PhotoImage(file=relative_to_assets("pause_button.png"))
play_button_img = PhotoImage(file=relative_to_assets("play_button.png"))

current_input_path = StringVar()
current_effect = StringVar()

record_button_img = PhotoImage(
    file=relative_to_assets("button_2.png"))
record_button = Button(
    image=record_button_img,
    cursor="hand2",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: toggle_recording(record_button),
    relief="flat"
)
record_button.place(
    x=388.0,
    y=113.0,
    width=140.0,
    height=52.0
)

file_select_img = PhotoImage(
    file=relative_to_assets("button_3.png"))
file_select_button = Button(
    image=file_select_img,
    cursor="hand2",
    borderwidth=0,
    highlightthickness=0,
    command=select_file,
    relief="flat"
)
file_select_button.place(
    x=570.0,
    y=113.0,
    width=140.0,
    height=52.0
)

settings_img = PhotoImage(
    file=relative_to_assets("button_4.png"))
settings_button = Button(
    image=settings_img,
    cursor='hand2',
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
settings_button.place(
    x=0.0,
    y=0.0,
    width=198.0,
    height=38.0
)

# NEW
save_file_img = PhotoImage(
    file=relative_to_assets("button_5.png"))
save_button = Button(
    image=save_file_img,
    borderwidth=0,
    highlightthickness=0,
    command=apply_effect,
    relief="flat"
)
save_button.place(
    x=934.0,
    y=113.0,
    width=140.0,
    height=52.0
)

settings_img_hover = PhotoImage(
    file=relative_to_assets("button_hover_1.png"))

def settings_hover(e):
    settings_button.config(
        image=settings_img_hover
    )
def settings_leave(e):
    settings_button.config(
        image=settings_img
    )

settings_button.bind('<Enter>', settings_hover)
settings_button.bind('<Leave>', settings_leave)

file_select_img_hover = PhotoImage(
    file=relative_to_assets("button_hover_2.png"))

def file_select_hover(e):
    file_select_button.config(
        image=file_select_img_hover
    )
def file_select_leave(e):
    file_select_button.config(
        image=file_select_img
    )

file_select_button.bind('<Enter>', file_select_hover)
file_select_button.bind('<Leave>', file_select_leave)

save_file_img_hover = PhotoImage(
    file=relative_to_assets("button_hover_3.png"))

def save_file_hover(e):
    save_button.config(
        image=save_file_img_hover
    )
def save_file_leave(e):
    save_button.config(
        image=save_file_img
    )

save_button.bind('<Enter>', save_file_hover)
save_button.bind('<Leave>', save_file_leave)

# Drop Down Menu

variable = tk.StringVar()
variable.set("Choose Effect")
list_effects = ['Echo', 'Reverb', 'Distortion', 'Tremolo', 'WahWah']

# Use 'window' as the parent for OptionMenu, not 'canvas'
effects_dropdown = tk.OptionMenu(
    window,
    variable,
    *list_effects,
    command=lambda effect: select_effect(effect)
)

dropdown_img = PhotoImage(
    file=relative_to_assets("dropdown.png"))
effects_dropdown.config(
    bg="#D9D9D9",
    fg="black",
    cursor='hand2',
    activebackground='#FF5C00',
    activeforeground='black',
    font=("Verdana", 16, 'bold'),
    borderwidth=0,
    border=0,
    highlightthickness=0,
    highlightcolor="#c1c6ee",
    pady=20,
    indicatoron=0
)

effects_dropdown['menu'].config(
    bg="#D9D9D9",
    fg="black",
    cursor='hand2',
    activebackground='#FF5C00',
    activeforeground='black',
    font=("Verdana", 14, 'bold'),
    borderwidth=0
)

# Place OptionMenu on the canvas at a specific location
effects_dropdown.place(
    x=0.0,
    y=113.0,
    width=280.0,
    height=52.0)

dropdown_label = tk.Label(
    effects_dropdown,
    width=25,
    height=25,
    borderwidth=0,
    border=0,
    highlightthickness=0,
    image=dropdown_img
)

dropdown_label.place(
    relx=0.87,
    rely=0.3
)

def dropdown_hover(event):
    dropdown_label.config(
        bg='#FF5C00'
    )
def dropdown_leave(event):
    dropdown_label.config(
        bg='white'
    )
effects_dropdown.bind('<Enter>', dropdown_hover)
effects_dropdown.bind('<Leave>', dropdown_leave)

def on_dropdown_click(event):
    x = effects_dropdown.winfo_rootx()
    y = effects_dropdown.winfo_rooty() + effects_dropdown.winfo_height()
    effects_dropdown['menu'].post(x, y)


dropdown_label.bind('<Button-1>', on_dropdown_click)

# Variables for effects
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)

entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)

entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)

entry_4 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)

text_1 = Label(
    font=("Inter Bold", 18 * -1),
    bg="#1897DF",
    fg="white"
)
text_2 = Label(
    font=("Inter Bold", 18 * -1),
    bg="#1897DF",
    fg="white"
)
text_3 = Label(
    font=("Inter Bold", 18 * -1),
    bg="#1897DF",
    fg="white"
)
text_4 = Label(
    font=("Inter Bold", 18 * -1),
    bg="#1897DF",
    fg="white"
)

def select_effect(effect):
    current_effect.set(effect)

    entry_1.place_forget()
    entry_2.place_forget()
    entry_3.place_forget()
    entry_4.place_forget()
    text_1.place_forget()
    text_2.place_forget()
    text_3.place_forget()
    text_4.place_forget()

    # ['Echo', 'Reverb', 'Distortion', 'Tremolo', 'WahWah']
    number_of_entries = None
    if effect == 'Echo':
        number_of_entries = 2
        text_1.config(text="Delay in s")
        text_2.config(text="Delay Amplifier in %")
    elif effect == 'Reverb':
        number_of_entries = 2
        text_1.config(text="Delay in s")
        text_2.config(text="Decay in %")
    elif effect == 'Distortion':
        number_of_entries = 2
        text_1.config(text="Gain in %")
        text_2.config(text="Threshold in %")
    elif effect == 'Tremolo':
        number_of_entries = 2
        text_1.config(text="Rate as integer")
        text_2.config(text="Depth in %")
    elif effect == 'WahWah':
        number_of_entries = 4
        text_1.config(text="LFO Frequency in Hz")
        text_2.config(text="Minimum Frequency in Hz")
        text_3.config(text="Maximum Frequency in Hz")
        text_4.config(text="Bandwidth in Hz")

    if number_of_entries >= 1:
        entry_1.place(
            x=388.0,
            y=271.0,
            width=255.0,
            height=42.0
        )
        text_1.place(
            x=388.0,
            y=238.0
        )
    if number_of_entries >= 2:
        entry_2.place(
            x=388.0,
            y=370.0,
            width=255.0,
            height=42.0
        )
        text_2.place(
            x=388.0,
            y=337.0
        )
    if number_of_entries >= 3:
        entry_3.place(
            x=388.0,
            y=469.0,
            width=255.0,
            height=42.0
        )
        text_3.place(
            x=388.0,
            y=436.0
        )
    if number_of_entries >= 4:
        entry_4.place(
            x=388.0,
            y=568.0,
            width=255.0,
            height=42.0
        )
        text_4.place(
            x=388.0,
            y=535.0
        )


window.resizable(False, False)
window.mainloop()
