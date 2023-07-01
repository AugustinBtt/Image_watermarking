from tkinter import filedialog
from watermarking import *
import tkinter as tk

def browse_image():
    global watermark_update
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])

    if file_path:
        original_img = Image.open(file_path)

        watermark_update = WatermarkImage(window, photo_box, original_img)
        watermark_update.watermark_instance = watermark

        watermark_update.update_image()


#---------------------------------------- UI --------------------------------------------------#

window = tk.Tk()
window.geometry("830x525")
window.title("Watermark editor")


watermark = Watermark()
watermark.text = ""

photo_box = ImageBox(window)
photo_box.grid(column=0, row=0, rowspan=5, padx=5)

watermark_update = WatermarkImage(window, photo_box, photo_box.grey_image)
watermark_update.watermark_instance = watermark


browse_button = tk.Button(window, text="Browse image", command=browse_image)
browse_button.grid(row=5, column=4, sticky='W', padx=10)


def save_command():
    global watermark_update
    watermark_update.save_image()

save_button = tk.Button(window, text="💾", command=save_command)
save_button.grid(row=5, column=4, sticky='E',padx=10)


text_label = tk.Label(text="Watermark text:")
text_label.grid(row=5, column=0, pady=5)

text_content = ''

def text_updated(*args):
    global text_content
    text_content = text_var.get()
    watermark_update.watermark_instance.text = text_content
    watermark_update.update_image()

text_var = tk.StringVar()
text_var.trace_add("write", text_updated)

watermark_text = tk.Entry(textvariable=text_var, width= 40)
watermark_text.grid(row=5, column=0, sticky='E', padx=5, pady=5)



opacity_var = tk.IntVar()
opacity_var.set(watermark.opacity)
opacity_scale = tk.Scale(window, from_=0, to=255, orient="horizontal", length=150, label="Opacity", variable=opacity_var)
opacity_scale.grid(row=1, column=4, padx=6, pady=6)

def on_opacity_change(*args):
    watermark.set_opacity(opacity_var.get())
    watermark_update.watermark_instance = watermark
    watermark_update.update_image()

# set up trace
opacity_var.trace("w", on_opacity_change)


def on_color_change(*args):
    color = color_var.get()
    color_dict = {
        'red': (255, 0, 0, watermark.opacity),
        'green': (0, 255, 0, watermark.opacity),
        'blue': (0, 0, 255, watermark.opacity),
        'yellow': (255, 255, 0, watermark.opacity),
        'grey': (128, 128, 128, watermark.opacity),
        'black': (0, 0, 0, watermark.opacity),
        'white': (255, 255, 255, watermark.opacity),
        'orange': (255, 165, 0, watermark.opacity),
        'purple': (128, 0, 128, watermark.opacity),
        'transparent': (0, 0, 0, watermark.opacity),
    }
    watermark.color = color_dict[color]
    watermark_update.watermark_instance = watermark
    watermark_update.update_image()

color_var = tk.StringVar()
color_var.set("white")  
color_var.trace("w", on_color_change)

color_option_menu = tk.OptionMenu(window, color_var, 'red', 'green', 'blue', 'yellow', 'grey', 'black', 'white', 'orange', 'purple', 'transparent')
color_option_menu.grid(row=0, column=4, padx=10, sticky='E')
color_label = tk.Label(window, text="Color")
color_label.grid(row=0, column=4, padx=20, sticky='W')




size_var = tk.IntVar()
size_var.set(watermark.font_size)
size_scale = tk.Scale(window, from_=1, to=120, orient="horizontal", length=150, label="Font size", variable=size_var)
size_scale.grid(row=2, column=4, padx=6, pady=6)

def on_size_change(*args):
    watermark.font_size = size_var.get()
    watermark_update.watermark_instance = watermark
    watermark_update.update_image()

size_var.trace('w', on_size_change)


def select_font(*args):
    font_name = font_var.get()
    font_dict = {
        'Arial' : "arial.ttf",
        'Aloevera': 'Aloevera.ttf',
        'AnandaBlack': 'AnandaBlack.ttf',
        'ArianaVioleta': 'ArianaVioleta.ttf',
        'Believelt': 'BelieveIt.ttf',
        'ChrustyRock': 'ChrustyRock.ttf',
        'Dattermatter': 'DattermatterBold.ttf',
        'NatureBeauty': 'NatureBeauty.ttf',
        'Songstar': 'Songstar.ttf',
        'Yacimiento': 'Yacimiento ExtraBold.ttf',
    }

    watermark.font = font_dict[font_name]
    watermark_update.watermark_instance = watermark
    watermark_update.update_image()

font_var = tk.StringVar()
font_var.set("arial.ttf")
font_var.trace("w", select_font)

font_option_menu = tk.OptionMenu(window, font_var, 'Arial', 'Aloevera', 'AnandaBlack', 'ArianaVioleta', 'Believelt', 'ChrustyRock', 'Dattermatter', 'NatureBeauty', 'Songstar', 'Yacimiento')
font_option_menu.grid(row=5, column=0, padx=5, sticky='W')



button_up = tk.Button(window, text="↑", command=lambda: (watermark.move_up(), watermark_update.update_image()))
button_down = tk.Button(window, text="↓", command=lambda: (watermark.move_down(), watermark_update.update_image()))
button_left = tk.Button(window, text="←", command=lambda: (watermark.move_left(), watermark_update.update_image()))
button_right = tk.Button(window, text="→", command=lambda: (watermark.move_right(), watermark_update.update_image()))

button_rotate_left = tk.Button(window, text="↶", command=lambda: (watermark.rotate_left(), watermark_update.update_image()))
button_rotate_right = tk.Button(window, text="↷", command=lambda: (watermark.rotate_right(), watermark_update.update_image()))
rotate_label = tk.Label(window, text="Rotate")

button_up.grid(row=3, column=4, sticky='N')
button_down.grid(row=3, column=4, sticky='S')
button_left.grid(row=3, column=4, sticky='W')
button_right.grid(row=3, column=4, sticky='E')
button_rotate_left.grid(row=4, column=4, sticky= 'W')
button_rotate_right.grid(row=4, column=4, sticky= "E")
rotate_label.grid(row=4, column=4)


window.mainloop()