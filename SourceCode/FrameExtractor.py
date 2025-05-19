import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import os
import tkinter.font as tkFont

# Constants
FONT_PATH = "fonts/CustomFont.ttf"  # Optional
CUSTOM_SIZES = [
    "640x480", "800x600", "1024x768",
    "1280x720", "1920x1080", "2560x1440"
]

# Global state
video_path = None
save_path = None  # Store custom save path

# GUI Setup
root = tk.Tk()
root.title("Video Frame Extractor")
root.geometry("460x420")
root.configure(bg="#1e1e1e")

# Create Tkinter variables after the root window is created
size_option = tk.StringVar(value="original")
selected_size = tk.StringVar(value=CUSTOM_SIZES[0])

# Load font or fallback
try:
    custom_font = tkFont.Font(file=FONT_PATH, size=13)
except:
    custom_font = ("Segoe UI", 12)

# Functions to handle video and frame extraction
def extract_frames():
    global video_path, save_path
    if not video_path:
        messagebox.showerror("Error", "Please select a video file first.")
        return
    if not save_path:
        messagebox.showerror("Error", "Please select a save path for the frames.")
        return

    cam = cv2.VideoCapture(video_path)
    if not cam.isOpened():
        messagebox.showerror("Error", "Could not open video file.")
        return

    os.makedirs(save_path, exist_ok=True)
    currentframe = 0

    # Custom size handling
    if size_option.get() == "custom":
        width, height = map(int, selected_size.get().split('x'))

    while True:
        ret, frame = cam.read()
        if ret:
            if size_option.get() == "custom":
                frame = cv2.resize(frame, (width, height))

            filename = os.path.join(save_path, f'frame{currentframe:04d}.jpg')
            cv2.imwrite(filename, frame)
            currentframe += 1
        else:
            break

    cam.release()
    messagebox.showinfo("Done", f"Extracted {currentframe} frames to {save_path}")

def browse_video():
    global video_path
    filetypes = [("Video Files", "*.mp4 *.avi *.mov *.mkv *.flv"), ("All Files", "*.*")]
    path = filedialog.askopenfilename(title="Select Video File", filetypes=filetypes)
    if path:
        video_path = path
        video_label.config(text=f"Selected: {os.path.basename(path)}")

def browse_save_path():
    global save_path
    save_path = filedialog.askdirectory(title="Select Save Folder")
    if save_path:
        save_path_label.config(text=f"Save Path: {save_path}")

# UI Elements
title = tk.Label(root, text="🎞️ Frame Extractor", font=custom_font, fg="white", bg="#1e1e1e")
title.pack(pady=10)

video_label = tk.Label(root, text="No video selected", fg="gray", bg="#1e1e1e")
video_label.pack()

browse_btn = tk.Button(root, text="Select Video", command=browse_video, font=custom_font,
                       bg="#3c3f41", fg="white", relief="flat", padx=10, pady=5)
browse_btn.pack(pady=10)

# Save Path
save_path_label = tk.Label(root, text="No save path selected", fg="gray", bg="#1e1e1e")
save_path_label.pack()

browse_save_btn = tk.Button(root, text="Select Save Path", command=browse_save_path, font=custom_font,
                            bg="#3c3f41", fg="white", relief="flat", padx=10, pady=5)
browse_save_btn.pack(pady=10)

# Size selection
size_frame = tk.Frame(root, bg="#1e1e1e")
size_frame.pack(pady=10)

tk.Label(size_frame, text="Frame Size Option:", bg="#1e1e1e", fg="white", font=custom_font).pack(anchor='w')

tk.Radiobutton(size_frame, text="Original Video Frame Size", variable=size_option, value="original",
               bg="#1e1e1e", fg="white", selectcolor="#2e2e2e", font=custom_font).pack(anchor='w')

tk.Radiobutton(size_frame, text="Custom Size", variable=size_option, value="custom",
               bg="#1e1e1e", fg="white", selectcolor="#2e2e2e", font=custom_font).pack(anchor='w')

# Dropdown for custom sizes
dropdown = ttk.Combobox(size_frame, textvariable=selected_size, values=CUSTOM_SIZES, state="readonly")
dropdown.pack(pady=5)

# Extract button
extract_btn = tk.Button(root, text="Extract Frames", command=extract_frames,
                        font=custom_font, bg="#4caf50", fg="white", relief="flat", padx=10, pady=10)
extract_btn.pack(pady=20)

root.mainloop()
