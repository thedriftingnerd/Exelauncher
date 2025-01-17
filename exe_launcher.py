import os
import subprocess
import json
from tkinter import Tk, filedialog, Button, Label, Entry, StringVar

CONFIG_FILE = "launcher_config.json"

def loadConfig():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE,"r") as file:
            return json.load(file)
    return {"wine_prefix": "", "recent_files": []}

def saveConfig():
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent = 4)

def exe_launcher():
    path = filedialog.askopenfilename(
        title = "Please select the Windows Executable file.",
        filetypes = [("Windows Executable Files", "*.exe")]
    )
    if path:

        wine_prefix = wine_prefix_var.get()
        wine_command = ["wine"]
        if wine_prefix:
            wine_command = ["env", f"WINEPREFIX={wine_prefix}"] + wine_command
        wine_command.append(path)

        try:
            subprocess.run(["wine", path], check = True)
            status_label.config(text = f"Executable Launched Successfully: {path}")

            if path not in config["recent_files"]:
                config["recent_files"].append(path)
                config["recent_files"] = config["recent files"][-5:]
                saveConfig(config)
        except subprocess.CalledProcessError as e:
            status_label.config(text = f"Executable Failed to Launch, please try again. If the problem persists, try launching the executable through the wine explorer via the terminal first a. {e}")
        except Exception as e:
            status_label.config(text = f"Error: {e}")

def recent(index):
    if 0 <= index < len(config["recent_files"]):
        path = config["recent_files"][index]
        wine_prefix = wine_prefix_var.get()
        wine_command = ["wine"]

        if wine_prefix:
            wine_command = ["env", f"WINEPREFIX = {wine_prefix}"] + wine_command

        wine_command.append(path)
        try:
            subprocess.run(wine_command, check = True)
            status_label.config(text = f"Executable Successfully Launched: {path}")
        except subprocess.CalledProcessError as e:
            status_label.config(text = f"Executable Failed to Launch, please try again. If the problem persists, try launching the executable through the wine explorer via the terminal first a. {e}")
        except Exception as e:
            status_label.config(text = f"Error: {e}")

config = loadConfig()

def update_wine_prefix(*args):
    config["wine_prefix"] = wine_prefix_var.get()
    saveConfig(config)

app = Tk()
app.title("Windows Executable Launcher")
app.geometry("600x400")

Label(app, text = "Optional Custom Wine Prefix", font = ("Ubuntu", 12)).pack(pady=5)
wine_prefix_var = StringVar()
wine_prefix_var.set(config.get("wine_prefix", ""))
wine_prefix_var.trace_add("write", update_wine_prefix)
Entry(app, textvariable=wine_prefix_var, width=50).pack(pady=5)

for i, path, in enumerate(config["recent_files"]):
    Button(app, text = os.path.basename(path), command = lambda i = 1: recent(i)).pack(pady=2)

Label(app, text = "Launch Windows executables on Linux", font = ("Ubuntu", 12)).pack(pady = 10)
Button(app, text="Select and Launch EXE", command = exe_launcher).pack(pady=20)
Entry(app, textvariable = wine_prefix_var, width = 50).pack(pady=5)

status_label = Label(app, text = "", wraplength = 300, fg = "blue")
status_label.pack(pady = 10)
app.mainloop() 