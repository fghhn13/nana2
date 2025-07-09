import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import colorsys
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

COLORS = {
    'bg_main': '#212121',
    'canvas_bg': '#212121',
    'slider_bg': '#414141',
    'slider_trough': '#515151',
    'label_fg': '#cbcbcb',
    'preview_bd': '#ffffff',
}

last_hex = None


def gen_hue_wheel(dia):
    data = np.zeros((dia, dia, 3), dtype=np.uint8)
    cx, cy = dia/2, dia/2
    r_max = dia/2
    for y in range(dia):
        for x in range(dia):
            dx, dy = x-cx, y-cy
            r = np.hypot(dx, dy)
            if r <= r_max:
                h = (np.degrees(np.arctan2(dy, dx)) + 360) % 360 / 360
                rgb = colorsys.hsv_to_rgb(h, 1.0, 1.0)
                data[y, x] = [int(255*c) for c in rgb]
    return Image.fromarray(data)


def gen_sv_square(size, hue, val):
    data = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            s = j/(size - 1)
            v = 1 - i/(size - 1)
            rgb = colorsys.hsv_to_rgb(hue, s, v * val)
            data[i, j] = [int(255*c) for c in rgb]
    return Image.fromarray(data)


def on_hue_click(evt):
    global cur_hue
    dx, dy = evt.x - wheel_r, evt.y - wheel_r
    if np.hypot(dx, dy) <= wheel_r:
        cur_hue = (np.degrees(np.arctan2(dy, dx)) + 360) % 360 / 360
        update_sv()


def on_sv_click(evt):
    if 0 <= evt.x < sv_size and 0 <= evt.y < sv_size:
        s = evt.x/(sv_size - 1)
        v = 1 - evt.y/(sv_size - 1)
        update_color(s, v * cur_val)


def on_val_change(val):
    global cur_val
    cur_val = float(val)
    update_sv()


def update_sv():
    global sv_tkimg
    img = gen_sv_square(sv_size, cur_hue, cur_val)
    sv_tkimg = ImageTk.PhotoImage(img)
    sv_canvas.itemconfig(sv_img_id, image=sv_tkimg)


def update_color(s, v):
    global last_hex
    r, g, b = [int(255*c) for c in colorsys.hsv_to_rgb(cur_hue, s, v)]
    hexc = f'#{r:02x}{g:02x}{b:02x}'
    last_hex = hexc
    preview.config(bg=hexc)
    lbl.config(text=f'RGB=({r},{g},{b})   HEX={hexc}')


def record_color():
    if last_hex:
        history_lb.insert(0, last_hex)
        history_lb.itemconfig(0, fg=last_hex)
        if history_lb.size() > 20:
            history_lb.delete(20, tk.END)


R = 8

def on_hue_drag(evt):
    hue_canvas.delete('marker')
    on_hue_click(evt)
    hue_canvas.create_line(
        evt.x-R, evt.y, evt.x+R, evt.y,
        fill='white', width=2, capstyle='butt', tags='marker'
    )
    hue_canvas.create_line(
        evt.x, evt.y-R, evt.x, evt.y+R,
        fill='white', width=2, capstyle='butt', tags='marker'
    )


def on_sv_drag(evt):
    sv_canvas.delete('marker')
    on_sv_click(evt)
    sv_canvas.create_line(
        evt.x-R, evt.y, evt.x+R, evt.y,
        fill='white', width=2, capstyle='butt', tags='marker'
    )
    sv_canvas.create_line(
        evt.x, evt.y-R, evt.x, evt.y+R,
        fill='white', width=2, capstyle='butt', tags='marker'
    )


wheel_dia = 300
wheel_r = wheel_dia // 2
sv_size = 300
cur_hue = 0.0
cur_val = 1.0

root = tk.Tk()
root.title("自由取色器 - lin酱版")
root.geometry('650x480')
root.config(bg=COLORS['bg_main'])
root.resizable(False, False)

hue_img = ImageTk.PhotoImage(gen_hue_wheel(wheel_dia))
hue_canvas = tk.Canvas(
    root, width=wheel_dia, height=wheel_dia,
    bg=COLORS['canvas_bg'], bd=0, highlightthickness=0
)
hue_canvas.grid(row=0, column=0, padx=10, pady=10)
hue_canvas.create_image(0, 0, anchor='nw', image=hue_img)
hue_canvas.bind('<Button-1>', on_hue_click)
hue_canvas.bind('<B1-Motion>', on_hue_drag)
hue_canvas.config(cursor='tcross')

sv_canvas = tk.Canvas(
    root, width=sv_size, height=sv_size,
    bg=COLORS['canvas_bg'], bd=0, highlightthickness=0
)
sv_canvas.grid(row=0, column=1, padx=10, pady=10)
sv_tkimg = None
sv_img_id = sv_canvas.create_image(0, 0, anchor='nw')
sv_canvas.bind('<Button-1>', on_sv_click)
sv_canvas.bind('<B1-Motion>', on_sv_drag)
sv_canvas.config(cursor='tcross')

val_slider = tk.Scale(
    root, bg=COLORS['slider_bg'], bd=0,
    from_=0.0, to=1.0, resolution=0.01,
    orient='horizontal', label='明度 (V)',
    fg=COLORS['label_fg'], troughcolor=COLORS['slider_trough'],
    highlightthickness=0, relief='flat', command=on_val_change
)
val_slider.set(1.0)
val_slider.grid(row=1, column=0, columnspan=2, sticky='we', padx=10)

preview = tk.Label(
    root, text="", bg=COLORS['bg_main'], bd=2,
    relief='solid', highlightbackground=COLORS['preview_bd']
)
preview.place(relx=0.05, rely=0.95, anchor='sw', width=40, height=40)
lbl = tk.Label(
    root, text="点击取色", font=("Arial", 14),
    fg=COLORS['label_fg'], bg=COLORS['bg_main']
)
lbl.grid(row=2, column=0, columnspan=2, pady=10)

history_win = tk.Toplevel(root)
history_win.title("历史取色记录")
history_win.geometry('360x530')
history_win.config(bg=COLORS['bg_main'])
history_win.resizable(False, False)

history_lb = tk.Listbox(
    history_win, bg=COLORS['slider_bg'], fg=COLORS['label_fg'],
    bd=1, highlightthickness=0, width=12, height=16
)
history_lb.pack(padx=10, pady=(10, 0), fill='both', expand=True)

record_btn = tk.Button(
    history_win, text='记录', command=record_color,
    bg=COLORS['slider_bg'], fg=COLORS['label_fg'], bd=0
)
record_btn.pack(side='bottom', pady=10, fill='x')

update_sv()
root.mainloop()
