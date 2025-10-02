import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys, os, json

DATA_FILE = "study_data.json"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS   # temp folder when running exe
    except Exception:
        base_path = os.path.abspath(".")  # current folder when running .py
    return os.path.join(base_path, relative_path)

# ---------- SAVE & LOAD ----------
def save_data():
    data = []
    for subject_frame in scroll_frame.winfo_children():
        header_frame = subject_frame.winfo_children()[0]
        subject_label = header_frame.winfo_children()[0].cget("text")
        
        units = []
        for widget in subject_frame.winfo_children()[1:]:
            if isinstance(widget, ctk.CTkCheckBox):
                units.append({"unit": widget.cget("text"), "done": widget.get() == 1})
        data.append({"subject": subject_label, "units": units})

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_data():
    if not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    for subject in data:
        create_subject(subject["subject"], subject["units"])

# ---------- GUI ----------
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Study Tracker")
app.geometry("700x500")
app.iconbitmap(resource_path("Logo.ico"))

# Main Heading
heading = ctk.CTkLabel(app, text="Study Tracker", font=("Inter", 22, "bold"))
heading.pack(pady=20)

# Inputs
input_frame = ctk.CTkFrame(app, fg_color="#232323", corner_radius=12)
input_frame.pack(pady=10, padx=20, fill="x")

subject_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter Subject")
subject_entry.pack(side="left", padx=10, pady=10)

units_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter Units (comma separated)")
units_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")

# Display Area
scroll_frame = ctk.CTkScrollableFrame(app, width=650, height=350, fg_color="#1e1e1e")
scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Delete subject function
def delete_subject(frame):
    frame.destroy()
    save_data()

# Create subject frame
def create_subject(subject, units_list):
    subject_frame = ctk.CTkFrame(scroll_frame, fg_color="#2a2a2a", corner_radius=10)
    subject_frame.pack(pady=10, padx=10, fill="x")

    # Header frame for subject name + delete button
    header_frame = ctk.CTkFrame(subject_frame, fg_color="transparent")
    header_frame.pack(fill="x", padx=10, pady=5)

    subject_label = ctk.CTkLabel(header_frame, text=subject, font=("Inter", 16, "bold"))
    subject_label.pack(side="left")

    trash_icon = ctk.CTkImage(light_image=Image.open(resource_path("bin.png")), size=(18, 18))

    del_button = ctk.CTkButton(
        header_frame, text='', image=trash_icon, width=15,
        fg_color="transparent", hover_color="#3a3a3a",
        command=lambda f=subject_frame: (delete_subject(f), save_data())
    )
    del_button.pack(side="right")

    # Unit checkboxes
    for unit_data in units_list:
        chk = ctk.CTkCheckBox(subject_frame, text=unit_data["unit"], fg_color="#7F48FF", text_color="white")
        chk.pack(anchor="w", padx=20, pady=10)
        if unit_data.get("done", False):
            chk.select()
        chk.configure(command=save_data)  # auto save when toggled

# Add subject function
def add_subject():
    subject = subject_entry.get().strip()
    units_text = units_entry.get().strip()

    if not subject or not units_text:
        messagebox.showwarning("Input Error", "Please enter both subject and units!")
        return

    units = [{"unit": u.strip(), "done": False} for u in units_text.split(",") if u.strip()]
    create_subject(subject, units)

    # Save after adding
    save_data()

    # Clear entries
    subject_entry.delete(0, "end")
    units_entry.delete(0, "end")

add_button = ctk.CTkButton(input_frame, text="Add Subject", fg_color="#7F48FF",
                           hover_color="#6B3CD9", command=add_subject)
add_button.pack(side="left", padx=10, pady=10)

# Load saved data on startup
load_data()

# Save before closing app
def on_closing():
    save_data()
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()