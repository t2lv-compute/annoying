import tkinter as tk
import random
import time

all_windows = []
shared_pixel_img = None

def spawn_window():
    global shared_pixel_img
    
    is_master = len(all_windows) == 0
    if is_master:
        root = tk.Tk()
        shared_pixel_img = tk.PhotoImage(width=1, height=1)
    else:
        root = tk.Toplevel(all_windows[0])
    
    root.title("Try to close me!")
    all_windows.append(root)
    
    # Movement State
    state = {"locked": False} 
    velocity = {"dx": random.choice([-1, 1]), "dy": random.choice([-1, 1])}

    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"300x120+{random.randint(100, sw-400)}+{random.randint(100, sh-300)}")
    root.resizable(False, False)
    root.attributes("-topmost", True)
    root.lift()

    def move_window():
        if state["locked"]: # Pause movement while loading grid
            root.after(10, move_window)
            return
        try:
            geom = root.geometry()
            main_part, x_str, y_str = geom.split('+')
            width, height = map(int, main_part.split('x'))
            x, y = int(x_str), int(y_str)

            if x + width >= sw or x <= 0: velocity["dx"] *= -1
            if y + height >= sh or y <= 0: velocity["dy"] *= -1

            root.geometry(f"+{max(0, min(x + velocity['dx'], sw - width))}+{max(0, min(y + velocity['dy'], sh - height))}")
            root.after(10, move_window)
        except:
            return

    def close_all():
        for win in list(all_windows):
            try: win.destroy()
            except: pass
        all_windows.clear()

    def on_savior():
        state["locked"] = True # Stop movement
        submit_btn.destroy()
        savior_btn.destroy()
        
        grid_frame = tk.Frame(root)
        grid_frame.pack(expand=True)

        rows, cols = 10, 10
        btn_count = [rows * cols]

        def hello(btn):
            if btn['state'] == 'disabled': return
            btn.config(state='disabled', bg="red")
            btn_count[0] -= 1
            if btn_count[0] <= 0:
                close_all()

        for i in range(cols):
            for j in range(rows):
                btn = tk.Button(grid_frame, image=shared_pixel_img, width=20, height=20, 
                               activebackground="yellow", bd=1, relief="raised")
                btn.bind("<Button-1>", lambda e, b=btn: hello(b))
                btn.grid(row=j, column=i)
        
        # Force the window to recognize the new buttons before moving again
        root.update_idletasks()
        root.geometry("") 
        root.after(1000, lambda: state.__setitem__("locked", False))

    def on_submit():
        spawn_window()
        if root == all_windows[0]:
            root.withdraw()
        else:
            if root in all_windows: all_windows.remove(root)
            root.destroy()

    submit_btn = tk.Button(root, text="Duplicate Window", font=("Courier", 18, "bold"), command=spawn_window)
    submit_btn.pack(fill="both", expand=True)

    savior_btn = tk.Button(root, text="Danger: Do Not Press", font=("Courier", 18, "bold underline"), command=on_savior,fg="white",bg="red")
    savior_btn.pack(fill="both", expand=True)

    move_window()
    root.bind("<Shift-Escape>", lambda e: close_all())
    root.protocol("WM_DELETE_WINDOW", on_submit)
    
    if is_master:
        root.mainloop()

if __name__ == "__main__":
    spawn_window()