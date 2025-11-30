import customtkinter as ctk
from tkinter import colorchooser
import colorsys

ctk.set_appearance_mode("light")

def rgb_to_cmyk(r, g, b):
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, 1
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255
    k = min(c, m, y)
    c = (c - k) / (1 - k)
    m = (m - k) / (1 - k)
    y = (y - k) / (1 - k)
    return round(c, 2), round(m, 2), round(y, 2), round(k, 2)

def cmyk_to_rgb(c, m, y, k):
    return (255*(1-c)*(1-k), 255*(1-m)*(1-k), 255*(1-y)*(1-k))

def rgb_to_hsv(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    return round(h*360), round(s*100), round(v*100)

def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h/360, s/100, v/100)
    return r*255, g*255, b*255

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Color Converter")
        self.geometry("500x750")

       

        self.preview = ctk.CTkFrame(self, height=70, width=400, corner_radius=20, fg_color="#ffe6f2")
        self.preview.pack(pady=5)
        self.preview.grid_propagate(False)

        self.color_box = ctk.CTkLabel(self.preview, text="", width=380, height=60,
                                      fg_color="#ffd9e8", corner_radius=16)
        self.color_box.grid(row=0, column=0, padx=10, pady=5)

        self.hex_text = ctk.CTkLabel(self, text="#ffd9e8",
                                     font=("SF Pro Display", 18, "bold"),
                                     text_color="#5c0033")
        self.hex_text.pack(pady=2)

        self.warn_label = ctk.CTkLabel(self, text="", text_color="red", font=("SF Pro", 12))
        self.warn_label.pack(pady=2)

        self.rgb_vars = [ctk.IntVar() for _ in range(3)]
        self.hsv_vars = [ctk.IntVar() for _ in range(3)]
        self.cmyk_vars = [ctk.DoubleVar() for _ in range(4)]

        self.create_block("RGB", ["R","G","B"], (0,255), self.rgb_vars, self.update_from_rgb, palette=True, palette_command=self.choose_color_rgb)
        self.create_block("HSV", ["H","S","V"], [(0,360),(0,100),(0,100)], self.hsv_vars, self.update_from_hsv, palette=True, palette_command=self.choose_color_hsv)
        self.create_block("CMYK", ["C","M","Y","K"], (0,1), self.cmyk_vars, self.update_from_cmyk, double=True, palette=True, palette_command=self.choose_color_cmyk)

    def warn(self, text):
        self.warn_label.configure(text=text)
        self.after(2500, lambda: self.warn_label.configure(text=""))

    def safe_update(self, var, command):
        try:
            float(var.get())
        except:
            return
        command()

    def create_block(self, title, labels, ranges, vars_list, command, double=False, palette=False, palette_command=None):
        frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#ffe6f2")
        frame.pack(padx=8, pady=4, fill="x")

        ctk.CTkLabel(frame, text=f"◆ {title}", font=("SF Pro Display", 16, "bold"),
                     text_color="#5c0033").pack(anchor="w", padx=8, pady=2)

        if palette:
            btn = ctk.CTkButton(frame, text="Choose the color", command=palette_command,
                                fg_color="#ffd6e8", hover_color="#ffb3d1", text_color="#5c0033", height=28)
            btn.pack(pady=4, padx=8, fill="x")

        for i, label in enumerate(labels):
            row = ctk.CTkFrame(frame, fg_color="#ffe6f2")
            row.pack(fill="x", padx=8, pady=2)

            ctk.CTkLabel(row, text=label, width=20, font=("SF Pro", 14, "bold"),
                         text_color="#5c0033").pack(side="left")

            rmin, rmax = ranges[i] if isinstance(ranges, list) else ranges
            slider = ctk.CTkSlider(row, from_=rmin, to=rmax,
                                   variable=vars_list[i],
                                   number_of_steps=255 if not double else 100,
                                   progress_color="#ffb3d1",
                                   button_color="#ff99c1",
                                   command=lambda e: command())
            slider.pack(side="left", fill="x", expand=True, padx=6)

            entry = ctk.CTkEntry(row, width=50, textvariable=vars_list[i],
                                 fg_color="#ffe6f2", text_color="#5c0033")
            entry.pack(side="right", padx=4)

            entry.bind("<Return>", lambda e, v=vars_list[i]: self.safe_update(v, command))
            entry.bind("<FocusOut>", lambda e, v=vars_list[i]: self.safe_update(v, command))

    def choose_color_rgb(self):
        color = colorchooser.askcolor()[0]
        if color:
            r, g, b = map(int, color)
            self.set_rgb(r, g, b)
            self.update_from_rgb()

    def choose_color_hsv(self):
        color = colorchooser.askcolor()[0]
        if color:
            r, g, b = map(int, color)
            h, s, v = rgb_to_hsv(r, g, b)
            for var, val in zip(self.hsv_vars, [h, s, v]):
                var.set(val)
            self.update_from_hsv()

    def choose_color_cmyk(self):
        color = colorchooser.askcolor()[0]
        if color:
            r, g, b = map(int, color)
            c, m, y, k = rgb_to_cmyk(r, g, b)
            for var, val in zip(self.cmyk_vars, [c, m, y, k]):
                var.set(val)
            self.update_from_cmyk()

    def set_rgb(self, r, g, b):
        for var, val in zip(self.rgb_vars, [r, g, b]):
            var.set(val)

    def update_visuals(self, r, g, b):
        hex_c = f"#{r:02x}{g:02x}{b:02x}"
        self.color_box.configure(fg_color=hex_c)
        self.hex_text.configure(text=hex_c)

    def update_from_rgb(self):
        r, g, b = [v.get() for v in self.rgb_vars]
        corrected = []
        clipped = False
        for x in (r, g, b):
            if x < 0 or x > 255:
                clipped = True
            corrected.append(min(255, max(0, int(x))))
        if clipped:
            self.warn("Out-of-range color detected — values were corrected")
        self.set_rgb(*corrected)
        c, m, y, k = rgb_to_cmyk(*corrected)
        h, s, v = rgb_to_hsv(*corrected)
        for var, val in zip(self.cmyk_vars, [c, m, y, k]):
            var.set(val)
        for var, val in zip(self.hsv_vars, [h, s, v]):
            var.set(val)
        self.update_visuals(*corrected)

    def update_from_cmyk(self):
        r, g, b = cmyk_to_rgb(*[v.get() for v in self.cmyk_vars])
        corrected = []
        clipped = False
        for x in (r, g, b):
            if x < 0 or x > 255:
                clipped = True
            corrected.append(min(255, max(0, int(x))))
        if clipped:
            self.warn("Out-of-range color detected — values were corrected")
        self.set_rgb(*corrected)
        self.update_from_rgb()

    def update_from_hsv(self):
        r, g, b = hsv_to_rgb(*[v.get() for v in self.hsv_vars])
        corrected = []
        clipped = False
        for x in (r, g, b):
            if x < 0 or x > 255:
                clipped = True
            corrected.append(min(255, max(0, int(x))))
        if clipped:
            self.warn("Out-of-range color detected — values were corrected")
        self.set_rgb(*corrected)
        self.update_from_rgb()

if __name__ == "__main__":
    app = App()
    app.mainloop()
