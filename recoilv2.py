import pyautogui
import time
import mouse
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from tkinter import ttk
from tkinter import PhotoImage
from pynput import keyboard
import os
import json
import requests

# Globale Variable, um das Programm zu steuern
running = True
movement_presets = []
shortcuts = {
    "start": "<ctrl>+<shift>+s",
    "pause": "<ctrl>+<shift>+p",
    "stop": "<ctrl>+<shift>+q"
}

# Lizenzüberprüfung
license_key = ""
server_url = "http://127.0.0.1:5000/check_license"

# Funktion zur Überprüfung der Lizenz
def check_license(key):
    try:
        response = requests.post(server_url, json={"license_key": key})
        response.raise_for_status()
        data = response.json()
        return data.get("valid", False)
    except requests.RequestException as e:
        messagebox.showerror("Fehler", f"Fehler bei der Lizenzüberprüfung: {e}")
        return False

# Funktion, um eine Lizenz einzugeben
def enter_license():
    global license_key
    license_key = simpledialog.askstring("Lizenz eingeben", "Bitte gib deinen Lizenzschlüssel ein:")
    if not license_key:
        messagebox.showwarning("Warnung", "Es wurde kein Lizenzschlüssel eingegeben.")
        return False
    if check_license(license_key):
        messagebox.showinfo("Erfolg", "Lizenz erfolgreich überprüft.")
        return True
    else:
        messagebox.showerror("Fehler", "Ungültiger Lizenzschlüssel.")
        return False

# Funktion, um ein einzelnes Preset aus einer Datei zu laden
def load_preset_from_file(filepath):
    with open(filepath, "r") as file:
        return json.load(file)

# Funktion, um ein einzelnes Preset in eine Datei zu speichern
def save_preset_to_file(preset, filename):
    with open(filename, "w") as file:
        json.dump(preset, file)

# Funktion, die die Maus basierend auf einem Preset bewegt
def on_click(movement):
    for move in movement:
        for _ in range(move[0]):
            pyautogui.moveRel(move[1], move[2], duration=0.1)  # Mausbewegung basierend auf Preset

# Funktion, die das Programm im Hintergrund laufen lässt
def background_loop():
    global running
    while running:
        if mouse.is_pressed(button='left'):
            if movement_presets:
                on_click(movement_presets[0])  # Benutze das erste Preset
        time.sleep(0.01)

# Tastenkombinationen zum Starten, Pausieren und Beenden des Programms
def on_start():
    global running
    running = True
    threading.Thread(target=background_loop, daemon=True).start()
    print("Programm gestartet.")
    messagebox.showinfo("Gestartet", "Das Programm wurde gestartet.")

def on_pause():
    global running
    running = False
    print("Programm pausiert.")
    messagebox.showinfo("Pausiert", "Das Programm wurde pausiert.")

def on_stop():
    global running
    running = False
    print("Programm wurde beendet.")
    messagebox.showinfo("Beendet", "Das Programm wurde gestoppt.")

# Eigener Interpreter zum Parsen der Befehle aus dem Editor
def parse_commands(commands):
    parsed_movements = []
    lines = commands.strip().splitlines()
    if len(lines) < 2 or lines[0].strip() != "START" or lines[-1].strip() != "END":
        raise ValueError("Die Befehle müssen mit START beginnen und mit END enden.")
    for line in lines[1:-1]:
        try:
            line = line.strip()
            if line.startswith("(") and line.endswith(")"):
                x, y = map(int, line[1:-1].split(","))
                parsed_movements.append((1, x, y))
            else:
                raise ValueError(f"Ungültiges Format in der Zeile: {line}")
        except (ValueError, IndexError):
            raise ValueError(f"Fehler beim Parsen der Zeile: {line}. Stelle sicher, dass das Format korrekt ist.")
    return parsed_movements

# Funktion zur Erstellung eines neuen Presets in einem separaten Fenster
def open_editor():
    editor_window = tk.Toplevel()
    editor_window.title("Preset Editor")
    editor_window.geometry("600x400")
    editor_window.configure(bg="#f0f0f0")

    ttk.Label(editor_window, text="Preset Befehle eingeben:", font=("Helvetica", 12), foreground="#000000", background="#f0f0f0").pack(pady=10)
    editor = scrolledtext.ScrolledText(editor_window, width=70, height=15, font=("Courier", 10), foreground="#000000", background="#ffffff")
    editor.insert(tk.END, "START\n(5,7)\n(-2,5)\nEND")
    editor.pack(pady=10)

    def save_preset():
        commands = editor.get("1.0", tk.END)
        try:
            preset = parse_commands(commands)
            preset_name = simpledialog.askstring("Preset Name", "Bitte einen Namen für das Preset eingeben:")
            if preset_name:
                filename = f"{preset_name}.json"
                save_preset_to_file(preset, filename)
                preset_list.insert(tk.END, preset_name)
                messagebox.showinfo("Erfolg", "Preset wurde gespeichert.")
                editor_window.destroy()
            else:
                messagebox.showwarning("Warnung", "Preset wurde nicht gespeichert. Kein Name angegeben.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Parsen der Befehle: {e}")

    ttk.Button(editor_window, text="Preset speichern", style='Accent.TButton', command=save_preset).pack(pady=5)

# Funktion zum Öffnen des Einstellungsmenüs
def open_settings():
    settings_window = tk.Toplevel()
    settings_window.title("Einstellungen")
    settings_window.geometry("500x400")
    settings_window.configure(bg="#f0f0f0")

    ttk.Label(settings_window, text="Tastenkombinationen konfigurieren:", font=("Helvetica", 12), foreground="#000000", background="#f0f0f0").pack(pady=10)

    def update_shortcut(action):
        new_shortcut = simpledialog.askstring("Shortcut ändern", f"Neuer Shortcut für {action}:")
        if new_shortcut:
            shortcuts[action] = new_shortcut
            shortcut_labels[action].config(text=f"{action.capitalize()}: {new_shortcut}")

    shortcut_labels = {}
    for action in shortcuts:
        frame = ttk.Frame(settings_window)
        frame.pack(pady=5, fill=tk.X)
        label = ttk.Label(frame, text=f"{action.capitalize()}: {shortcuts[action]}", font=("Helvetica", 10), foreground="#000000", background="#f0f0f0")
        label.pack(side=tk.LEFT, padx=10)
        shortcut_labels[action] = label
        ttk.Button(frame, text="Ändern", command=lambda a=action: update_shortcut(a)).pack(side=tk.RIGHT)

    def show_instructions():
        instructions = ("Anleitung:\n"
                        "1. Klicke auf 'Preset erstellen', um ein neues Preset hinzuzufügen.\n"
                        "2. Verwende die Befehle im Editor:\n"
                        "   - START: Beginnt die Befehlsdefinition.\n"
                        "   - END: Beendet die Befehlsdefinition.\n"
                        "   - (x,y): Bewegt die Maus um x Pixel horizontal und y Pixel vertikal.\n"
                        "3. Lade ein Preset, um es zu verwenden.\n"
                        "4. Beende das Programm mit den konfigurierten Shortcuts.")
        messagebox.showinfo("Anleitung", instructions)

    ttk.Button(settings_window, text="Anleitung anzeigen", style='Accent.TButton', command=show_instructions).pack(pady=10)

# Funktion zum Herunterladen von Presets von GitHub
def download_presets_from_github():
    url = "https://api.github.com/repos/LopeKinz/mouseflow_presets/contents"
    try:
        response = requests.get(url)
        response.raise_for_status()
        files = response.json()

        # Erstelle ein Auswahlfenster für die Presets
        download_window = tk.Toplevel()
        download_window.title("Presets von GitHub herunterladen")
        download_window.geometry("500x400")
        download_window.configure(bg="#f0f0f0")

        ttk.Label(download_window, text="Wähle die Presets aus, die du herunterladen möchtest:", font=("Helvetica", 12), foreground="#000000", background="#f0f0f0").pack(pady=10)

        presets_listbox = tk.Listbox(download_window, selectmode=tk.MULTIPLE, font=("Helvetica", 10), foreground="#000000", background="#f0f0f0")
        presets_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

        for file in files:
            if file["name"].endswith(".json"):
                presets_listbox.insert(tk.END, file["name"])

        def download_selected_presets():
            selected_indices = presets_listbox.curselection()
            if selected_indices:
                for index in selected_indices:
                    preset_name = presets_listbox.get(index)
                    preset_content = requests.get(files[index]["download_url"]).text
                    with open(preset_name, "w") as preset_file:
                        preset_file.write(preset_content)
                    preset_list.insert(tk.END, preset_name.replace(".json", ""))
                messagebox.showinfo("Erfolg", "Ausgewählte Presets wurden erfolgreich von GitHub heruntergeladen.")
                download_window.destroy()
            else:
                messagebox.showwarning("Warnung", "Bitte wähle mindestens ein Preset aus.")

        ttk.Button(download_window, text="Ausgewählte Presets herunterladen", style='Accent.TButton', command=download_selected_presets).pack(pady=10)

    except requests.RequestException as e:
        messagebox.showerror("Fehler", f"Fehler beim Herunterladen der Presets: {e}")

# GUI zur Verwaltung von Presets
def open_gui():
    global preset_list

    if not enter_license():
        return

    root = tk.Tk()
    root.title("Pinky's AntiRecoil V1")
    root.geometry("600x600")
    root.configure(bg="#f0f0f0")

    # Füge ein Logo hinzu
    # logo = PhotoImage(file="logo.png")  # Beispiel: eigenes Logo hinzufügen
    # ttk.Label(root, image=logo).pack(pady=10)

    ttk.Label(root, text="Pinky's AntiRecoil V1", font=("Helvetica", 18, "bold"), foreground="#000000").pack(pady=10)

    def add_preset():
        open_editor()

    def load_preset():
        selected = preset_list.curselection()
        if selected:
            preset_name = preset_list.get(selected[0])
            filename = f"{preset_name}.json"
            if os.path.exists(filename):
                preset = load_preset_from_file(filename)
                movement_presets.insert(0, preset)  # Setzt das gewählte Preset an die erste Stelle
                messagebox.showinfo("Geladen", f"Preset '{preset_name}' wurde geladen.")
            else:
                messagebox.showerror("Fehler", "Die Datei für das ausgewählte Preset wurde nicht gefunden.")
        else:
            messagebox.showwarning("Warnung", "Bitte wähle ein Preset aus.")

    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="Preset erstellen", style='Accent.TButton', command=add_preset).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Preset laden", style='Accent.TButton', command=load_preset).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Einstellungen", style='Accent.TButton', command=open_settings).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(button_frame, text="Presets von GitHub herunterladen", style='Accent.TButton', command=download_presets_from_github).grid(row=0, column=3, padx=5, pady=5)

    ttk.Label(root, text="Verfügbare Presets:", font=("Helvetica", 14), foreground="#000000").pack(pady=5)
    preset_list = tk.Listbox(root, height=10, font=("Helvetica", 10), foreground="#000000", background="#f0f0f0")
    preset_list.pack(pady=5, fill=tk.BOTH, expand=True)

    # Lade Presets in die Liste
    for filename in os.listdir():
        if filename.endswith(".json"):
            preset_list.insert(tk.END, filename.replace(".json", ""))

    root.mainloop()

# Starte den GUI-Thread
threading.Thread(target=open_gui, daemon=True).start()

# Setze eine Tastenkombination zum Starten, Pausieren und Beenden (initiale Werte)
with keyboard.GlobalHotKeys({
    shortcuts["start"]: on_start,
    shortcuts["pause"]: on_pause,
    shortcuts["stop"]: on_stop
}) as listener:
    listener.join()
