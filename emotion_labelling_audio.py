import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from playsound import playsound
import os
import json

class AudioViewer2(tk.Tk):
    def __init__(self, root, json_path):
        super().__init__()
        self.title("Audio Viewer")
        self.geometry("1340x500")
        self.clip_index = 0
        self.clips = []
        self.settings = {}
        self.root_dir = root
        self.json_file = json_path
        with open(json_path, 'r') as file:
            data = json.load(file)
        self.clips = [entry['filename'] for entry in data]
        self.create_widgets()
        self.style = ttk.Style()
        self.style.configure('.', font=('Helvetica', 12))

    def create_widgets(self):
        self.nav_frame = ttk.Frame(self)
        self.nav_frame.pack(side=tk.LEFT, fill=tk.BOTH, pady=10, padx=10)

        self.nav_panel = ttk.Frame(self.nav_frame)
        self.nav_panel.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.text_box = tk.Text(self.nav_panel, wrap='word', font=("Helvetica", 13), height=2, width=30)
        self.text_box.pack(side=tk.TOP, expand=True, padx=10, pady=10)

        self.play_button = ttk.Button(self.nav_panel, text="Play", command=self.play_track)
        self.play_button.pack(fill=tk.BOTH, side=tk.TOP)

        self.prev_button = ttk.Button(self.nav_panel, text="Previous", command=self.play_previous_clip)
        self.prev_button.pack(fill=tk.X, side=tk.LEFT, padx=10, pady=10)

        self.save_button = ttk.Button(self.nav_panel, text="Save", command=self.save_settings)
        self.save_button.pack(fill=tk.X, side=tk.LEFT, padx=10, pady=10)

        self.clear_button = ttk.Button(self.nav_panel, text="Clear", command=self.clear_settings)
        self.clear_button.pack(fill=tk.X, side=tk.LEFT, padx=10, pady=10)

        self.next_button = ttk.Button(self.nav_panel, text="Next", command=self.play_next_clip)
        self.next_button.pack(fill=tk.X, side=tk.LEFT, padx=10, pady=10)

        self.settings_frame = ttk.Frame(self)
        self.settings_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.chars = ['Sunny', 'Izzy', 'Pipp', 'Zipp', 'Hitch', 'Misty', 'Sprout', 'Opaline', 'Queen', 'Alphabittle']
        self.emotions = ['casual', 'happy', 'surprise', 'discontent', 'sad', 'smug']

        for emotion in self.emotions:
            self.emotion_frame = ttk.Labelframe(self.settings_frame, text=emotion.capitalize())
            self.emotion_frame.pack(side=tk.LEFT, fill='x', padx=10, pady=10)
            self.char_buttons = []

            for i in range(0, len(self.chars)):
                self.char_button = ttk.Button(self.emotion_frame, text=f'{self.chars[i]}', command=lambda i=i, emotion=emotion: self.log_emotion(f'{self.chars[i]}', emotion))
                self.char_button.pack(fill='x', padx=5, pady=5)
                self.char_buttons.append(self.char_button)

        self.bind('<Right>', lambda event: self.play_next_clip())
        self.bind('<Left>', lambda event: self.play_previous_clip())
        self.bind('<BackSpace>', lambda event: self.clear_settings())
        self.bind('<space>', lambda event: self.play_track())
        self.load_settings()

    def play_track(self):
        playsound(self.audio_path)

    def log_emotion(self, char, emotion):
        self.text_box.insert('end', f"{char}:{emotion}, ")
        self.char.append(char)
        self.emo.append(emotion)

    def clear_settings(self):
        self.char = []
        self.emo = []
        self.text_box.delete(1.0, tk.END)

    def play_previous_clip(self):
        self.clip_index = (self.clip_index - 1) % len(self.clips)
        self.load_settings()

    def play_next_clip(self):
        self.clip_index = (self.clip_index + 1) % len(self.clips)
        self.load_settings()

    def load_settings(self):
        self.audio_path = os.path.join(self.root_dir, self.clips[self.clip_index])
        characters = []
        emotions = []
        self.text_box.delete(1.0, tk.END)
        with open(self.json_file, 'r') as file:
            data = json.load(file)
        for line in data:
            if line['filename'] == self.clips[self.clip_index]:
                for key in line:
                    if key in self.chars:
                        emotion = line[key]
                        self.text_box.insert('end', f"{key}:{emotion}, ")
                        characters.append(key)
                        emotions.append(emotion)
        self.char = characters
        self.emo = emotions
        self.play_track()

    def save_settings(self):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
        new_data = []
        for line in data:
            entry = line
            for key in line:
                if key == 'filename':
                    if line[key] == self.clips[self.clip_index]:
                        new_entry = {"filename": self.clips[self.clip_index]}
                        new_entry.update({ch: em for ch, em in zip(self.char, self.emo)})
                        entry = new_entry
            new_data.append(entry)
        print(new_entry)
        with open(self.json_file, 'w') as file:
            json.dump(new_data, file, indent=4)

def create_json(root, json_path):
    data = []
    clips = [f for f in os.listdir(root) if f.endswith(('wav', 'mp3', 'flac'))]
    clips = sorted(clips)
    for clip in clips:
        entry = {"filename": os.path.join(clip)}
        data.append(entry)
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    print("Select audio directory")
    root_directory = filedialog.askdirectory()
    ask_save = input("Would you like to create a .json file? (yes/no): ")
    if ask_save.lower() == 'yes':
        print("Save json path")
        json_file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        create_json(root_directory, json_file)
    else:
        print("Load json path")
        json_file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])

    app = AudioViewer2(root_directory, json_file)
    app.mainloop()
