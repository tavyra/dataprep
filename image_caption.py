import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import json

class ImageViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Viewer")
        self.image_paths = [""]
        self.current_index = 0
        self.captions = [""]

        self.load_button = tk.Button(self.master, text="Load Images", command=self.load_images)
        self.load_button.pack()

        self.image_label = tk.Label(self.master)
        self.image_label.pack()

        self.text_box = tk.Text(self.master, height=5, width=40)
        self.text_box.pack()

        self.prev_button = tk.Button(self.master, text="Previous", command=self.show_previous_image)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.master, text="Next", command=self.show_next_image)
        self.next_button.pack(side=tk.RIGHT)

        self.save_button = tk.Button(self.master, text="Save", command=self.save_data)
        self.save_button.pack(side=tk.BOTTOM)

        self.load_images()

    def load_images(self):
        self.root_dir = filedialog.askdirectory()
        ask_save = input("Would you like to create captions.json? This will overwrite existing file (yes/no): ")
        self.json_path = os.path.join(self.root_dir, "captions.json")
        self.captions = []
        self.image_paths = []
        if ask_save.lower() == "yes":
            entries = []
            for item in os.listdir(self.root_dir):
                if os.path.isfile(os.path.join(self.root_dir, item)) and item.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webm', '.webp')):
                    self.image_paths.append(item)
            self.image_paths = sorted(self.image_paths)
            for image in self.image_paths:
                self.captions.append("")
                entry = {"images": image, "caption": ""}
                entries.append(entry)
            with open(self.json_path, "w") as f:
                json.dump(entries, f, indent = 4)
        elif ask_save.lower() == "no":
            with open(self.json_path, "r") as f:
                data = json.load(f)
                for line in data:
                    for key in line:
                        if key == "images":
                            self.image_paths.append(line[key])
                        elif key == "caption":
                            self.captions.append(line[key])
                        else:
                            print("unexpected data item will be overwritten upon save")
                for filename, caption in data:
                    self.image_paths.append(filename)
                    self.captions.append(caption)
        else:
            print("failed to load _")
        self.load_image()

    def load_image(self):
        image_path = os.path.join(self.root_dir, self.image_paths[self.current_index])
        image = Image.open(image_path)
        image = image.resize((720, 480), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        try:
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, self.captions[self.current_index])
        except FileNotFoundError:
            print("captions.json has not been created")

    def show_previous_image(self):
        self.captions[self.current_index] = self.text_box.get(1.0, tk.END).strip()
        self.current_index = (self.current_index - 1) % len(self.image_paths)
        self.load_image()

    def show_next_image(self):
        self.captions[self.current_index] = self.text_box.get(1.0, tk.END).strip()
        self.current_index = (self.current_index + 1) % len(self.image_paths)
        self.load_image()

    def save_data(self):
        self.captions[self.current_index] = self.text_box.get(1.0, tk.END).strip()
        new_entry = {"images": self.image_paths[self.current_index], "caption": self.captions[self.current_index]}
        print("saving ", new_entry)
        with open(self.json_path, "r") as file:
            data = json.load(file)
        new_data = []
        for line in data:
            new_line = line
            for key in line:
                if key == 'images':
                    if line[key] == self.image_paths[self.current_index]:
                        new_line = new_entry
            new_data.append(new_line)
        with open(self.json_path, "w") as f:
            json.dump(new_data, f, indent = 4)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()
