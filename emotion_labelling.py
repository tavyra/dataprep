import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
from PIL import Image, ImageTk

class ImageViewer2(tk.Tk):
    def __init__(self, root, json_path):
        super().__init__()
        self.title("Image Viewer")
        self.geometry("2160x1040")
        self.image_index = 0
        self.images = []
        self.settings = {}
        self.root_dir = root
        self.json_file = json_path
        with open(json_path, 'r') as file:
            data = json.load(file)
        #for filename, tags in data.items():
        #    self.images.append(filename)
        self.images = [entry['filename'] for entry in data]
        self.create_widgets()
        self.style = ttk.Style()
        self.style.configure('.', font=('Helvetica', 12))

    def create_widgets(self):
        self.image_frame = ttk.Frame(self)
        self.image_frame.pack(side=tk.LEFT, fill=tk.BOTH, pady=10, padx=10)

        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=10)

        self.nav_panel = ttk.Frame(self.image_frame)
        self.nav_panel.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)

        self.text_box = tk.Text(self.image_frame, wrap='word', font=("Helvetica", 13), height=10, width=30)
        self.text_box.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True, padx=10, pady=10)

        self.prev_button = ttk.Button(self.nav_panel, text="Previous", command=self.show_previous_image)
        self.prev_button.pack(fill=tk.X, side=tk.TOP, padx=10, pady=10)

        self.save_button = ttk.Button(self.nav_panel, text="Save", command=self.save_settings)
        self.save_button.pack(fill=tk.X, side=tk.TOP, padx=10, pady=10)

        self.clear_button = ttk.Button(self.nav_panel, text="Clear", command=self.clear_settings)
        self.clear_button.pack(fill=tk.X, side=tk.TOP, padx=10, pady=10)

        self.next_button = ttk.Button(self.nav_panel, text="Next", command=self.show_next_image)
        self.next_button.pack(fill=tk.X, side=tk.TOP, padx=10, pady=10)

        self.settings_frame = ttk.Frame(self)
        self.settings_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.chars = ['Twilight', 'Pinkie', 'Rainbow', 'Fluttershy', 'Rarity', 'Applejack', 'Spike', 'Starlight', 'Trixie', 'Maud', 'Sunburst', 'Shining', 'Apple', 'Scootaloo', 'Sweetie', 'Celestia', 'Luna', 'Cadance', 'Discord', 'Chrysalis', 'Cheerilee', 'Zecora']
        self.emotions = ['casual', 'happy', 'surprise', 'discontent', 'sad', 'smug']

        for emotion in self.emotions:
            self.emotion_frame = ttk.Labelframe(self.settings_frame, text=emotion.capitalize())
            self.emotion_frame.pack(side=tk.LEFT, fill='x', padx=10, pady=10)
            self.char_buttons = []

            for i in range(0, len(self.chars)):
                self.char_button = ttk.Button(self.emotion_frame, text=f'{self.chars[i]}', command=lambda i=i, emotion=emotion: self.log_emotion(f'{self.chars[i]}', emotion))
                self.char_button.pack(fill='x', padx=5, pady=5)
                self.char_buttons.append(self.char_button)

        self.load_image()

    def load_image(self):
        self.image_path = os.path.join(self.root_dir, self.images[self.image_index])
        image = Image.open(self.image_path)
        image = image.resize((1280, 720), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.photo)
        self.image_label.image = self.photo
        self.load_settings()

    def log_emotion(self, char, emotion):
        self.text_box.insert('end', f"{char}:{emotion}, ")
        self.char.append(char)
        self.emo.append(emotion)

    def clear_settings(self):
        self.char = []
        self.emo = []
        self.text_box.delete(1.0, tk.END)

    def show_previous_image(self):
        self.image_index = (self.image_index - 1) % len(self.images)
        self.load_image()

    def show_next_image(self):
        self.image_index = (self.image_index + 1) % len(self.images)
        self.load_image()

    def load_settings(self):
        characters = []
        emotions = []
        self.text_box.delete(1.0, tk.END)
        with open(self.json_file, 'r') as file:
            data = json.load(file)
        for line in data:
            if line['filename'] == self.images[self.image_index]:
                for key in line:
                    if key in self.chars:
                        emotion = line[key]
                        self.text_box.insert('end', f"{key}:{emotion}, ")
                        characters.append(key)
                        emotions.append(emotion)
        self.char = characters
        self.emo = emotions

    def save_settings(self):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
        new_data = []
        for line in data:
            entry = line
            for key in line:
                if key == 'filename':
                    if line[key] == self.images[self.image_index]:
                        new_entry = {"filename": self.images[self.image_index]}
                        new_entry.update({ch: em for ch, em in zip(self.char, self.emo)})
                        entry = new_entry
            new_data.append(entry)
        print(new_entry)
        with open(self.json_file, 'w') as file:
            json.dump(new_data, file, indent=4)

def create_json(root, json_path):
    data = []
    images = [f for f in os.listdir(root) if f.endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'webm'))]
    images = sorted(images)
    for image in images:
        entry = {"filename": os.path.join(image)}
        data.append(entry)
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    print("Select image directory")
    root_directory = filedialog.askdirectory()
    ask_save = input("Would you like to create a .json file? (yes/no): ")
    if ask_save.lower() == 'yes':
        print("Save json path")
        json_file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        create_json(root_directory, json_file)
    else:
        print("Load json path")
        json_file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])

    app = ImageViewer2(root_directory, json_file)
    app.mainloop()
