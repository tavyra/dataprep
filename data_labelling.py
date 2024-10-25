import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import json
from PIL import Image, ImageTk

class ImageViewer(tk.Tk):
    def __init__(self, root_directory, json_path):
        super().__init__()
        self.title("Image Viewer")
        self.geometry("1400x800")
        self.root_directory = root_directory
        self.json_file = json_path
        self.current_index = 0
        with open(json_path, 'r') as file:
            data = json.load(file)
            self.images = [entry['images'] for entry in data]
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self)
        self.label.pack(fill=tk.BOTH, expand=True)

        self.go_button = tk.Button(self, text="Go", font=("Helvetica", 13), command=self.move_index)
        self.go_button.pack(side=tk.LEFT)

        self.indexbox = tk.Entry(self, font=("Helvetica", 13), width=4)
        self.indexbox.pack(side=tk.LEFT)

        self.using_magic = tk.BooleanVar()
        self.magiccheck = tk.Checkbutton(self, text="Magic", font=("Helvetica", 13), variable=self.using_magic, command=self.toggle_magic)
        self.magiccheck.pack(side=tk.LEFT)

        self.is_flying = tk.BooleanVar()
        self.flyingcheck = tk.Checkbutton(self, text="Flying", font=("Helvetica", 13), variable=self.is_flying, command=self.toggle_flying)
        self.flyingcheck.pack(side=tk.LEFT)

        self.pony_button = tk.Button(self, text="Pony", font=("Helvetica", 13), command=lambda: self.increment_count("pony"))
        self.pony_button.pack(side=tk.LEFT)

        self.pony_label = tk.Text(self, font=("Helvetica", 13), height=1, width=2)
        self.pony_label.pack(side=tk.LEFT)

        self.unicorn_button = tk.Button(self, text="Unicorn", font=("Helvetica", 13), command=lambda: self.increment_count("unicorn"))
        self.unicorn_button.pack(side=tk.LEFT)

        self.unicorn_label = tk.Text(self, font=("Helvetica", 13), height=1, width=2)
        self.unicorn_label.pack(side=tk.LEFT)

        self.pegasus_button = tk.Button(self, text="Pegasus", font=("Helvetica", 13), command=lambda: self.increment_count("pegasus"))
        self.pegasus_button.pack(side=tk.LEFT)

        self.pegasus_label = tk.Text(self, font=("Helvetica", 13), height=1, width=2)
        self.pegasus_label.pack(side=tk.LEFT)

        self.species_var = tk.StringVar()
        self.feral_radio = tk.Radiobutton(self, text="Feral", font=("Helvetica", 13), variable=self.species_var, value="feral")
        self.feral_radio.pack(side=tk.LEFT)

        self.anthro_radio = tk.Radiobutton(self, text="Anthro", font=("Helvetica", 13), variable=self.species_var, value="anthro")
        self.anthro_radio.pack(side=tk.LEFT)

        self.other_radio = tk.Radiobutton(self, text="Other", font=("Helvetica", 13), variable=self.species_var, value="other")
        self.other_radio.pack(side=tk.LEFT)

        self.save_button = tk.Button(self, text="Save", font=("Helvetica", 13), command=self.save_alt)
        self.save_button.pack(side=tk.LEFT)

        self.load_button = tk.Button(self, text="Reload", font=("Helvetica", 13), command=self.load_data)
        self.load_button.pack(side=tk.LEFT)

        self.forward_button = tk.Button(self, text="Forward", font=("Helvetica", 13), command=self.show_next_image)
        self.forward_button.pack(side=tk.RIGHT)

        self.index_label = tk.Text(self, font=("Helvetica", 13), height=1, width=4)
        self.index_label.pack(side=tk.RIGHT)

        self.backward_button = tk.Button(self, text="Backward", font=("Helvetica", 13), command=self.show_previous_image)
        self.backward_button.pack(side=tk.RIGHT)

        self.bind('<Right>', lambda event: self.show_next_image())
        self.bind('<Left>', lambda event: self.show_previous_image())
        self.bind('<BackSpace>', lambda event: self.load_data())
        self.bind('m', lambda event: self.using_magic.set(True))
        self.bind('l', lambda event: print("uwu"))
        self.bind('p', lambda event: self.is_flying.set(True))
        self.bind('a', lambda event: self.species_var.set("feral"))
        self.bind('s', lambda event: self.species_var.set("anthro"))
        self.bind('d', lambda event: self.species_var.set("other"))
        self.bind('`', lambda event: self.species_var.set("0"))
        self.bind('q', lambda event: self.increment_count("pony"))
        self.bind('w', lambda event: self.increment_count("unicorn"))
        self.bind('e', lambda event: self.increment_count("pegasus"))

        self.load_data()

    def show_next_image(self):
        self.current_index = (self.current_index + 1) % len(self.images)
        self.load_data()

    def show_previous_image(self):
        self.current_index = (self.current_index - 1) % len(self.images)
        self.load_data()

    def move_index(self):
        try:
            new_index = int(self.indexbox.get())
            if 0 <= new_index < len(self.images):
                self.current_index = new_index
                self.load_data()
            else:
                self.indexbox = None
                messagebox.showerror("Error", "Invalid index")
        except ValueError:
                print("Enter a valid index")
                self.indexbox.delete(tk.END)

    def update_image(self):
        image_path = os.path.join(root_directory, self.images[self.current_index])
        try:
            image = Image.open(image_path)
        except(ValueError):
            print("File not found: ", image_path)

        image = image.resize((1280, 720), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.label.config(image=photo)
        self.label.image = photo

    def toggle_magic(self):
        self.magic = self.using_magic.get()

    def toggle_flying(self):
        self.flying = self.is_flying.get()

    def increment_count(self, creature):
        if creature == "pony":
            self.pony_count += 1
            self.pony_label.delete(1.0, tk.END)
            self.pony_label.insert(1.0, self.pony_count)
        elif creature == "unicorn":
            self.unicorn_count += 1
            self.unicorn_label.delete(1.0, tk.END)
            self.unicorn_label.insert(1.0, self.unicorn_count)
        elif creature == "pegasus":
            self.pegasus_count += 1
            self.pegasus_label.delete(1.0, tk.END)
            self.pegasus_label.insert(1.0, self.pegasus_count)

    def save_alt(self):
        species = self.species_var.get()
        entry = {"images":self.images[self.current_index], "magic":self.magic, "flying":self.flying, "pony_count":self.pony_count, "unicorn_count":self.unicorn_count, "pegasus_count":self.pegasus_count, "selected_species":species}
        with open(self.json_file, "r") as file:
            data = json.load(file)
        temp = []
        for entry in data:
            if entry['images'] == self.images[self.current_index]:
                #entry["magic"] = self.magic
                #entry["flying"] = self.flying
                #entry["pony_count"] = self.pony_count
                #entry["unicorn_count"] = self.unicorn_count
                #entry["pegasus_count"] = self.pegasus_count
                #entry["selected_species"] = self.selected_species
                new = {"images":self.images[self.current_index], "magic":self.magic, "flying":self.flying, "pony_count":self.pony_count, "unicorn_count":self.unicorn_count, "pegasus_count":self.pegasus_count, "selected_species":species}
                saved = new
            else:
                new = entry
            temp.append(new)
        with open(self.json_file, 'w') as file:
            json.dump(temp, file, indent=4)
        print("saved ", saved)

    def load_data(self):
        self.index_label.delete(1.0, tk.END)
        self.pony_label.delete(1.0, tk.END)
        self.unicorn_label.delete(1.0, tk.END)
        self.pegasus_label.delete(1.0, tk.END)
        print(self.images[self.current_index])
        with open(self.json_file, 'r') as file:
            data = json.load(file)
        for entry in data:
            if entry["images"] == self.images[self.current_index]:
                self.magic = entry["magic"]
                self.flying = entry["flying"]
                self.pony_count = entry["pony_count"]
                self.unicorn_count = entry["unicorn_count"]
                self.pegasus_count = entry["pegasus_count"]
                self.selected_species = entry["selected_species"]
                break
        self.species_var.set(self.selected_species)
        self.using_magic.set(self.magic)
        self.is_flying.set(self.flying)
        self.index_label.insert(1.0, self.current_index)
        self.unicorn_label.insert(1.0, self.unicorn_count)
        self.pony_label.insert(1.0, self.pony_count)
        self.pegasus_label.insert(1.0, self.pegasus_count)
        self.update_image()

    def reload_legacy(self):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
            self.magic = data["magic"]
            self.flying = data["flying"]
            self.pony_count = data["pony_count"]
            self.unicorn_count = data["unicorn_count"]
            self.pegasus_count = data["pegasus_count"]
            self.selected_species = data["selected_species"]
            self.images = data["images"]
        self.species_var.set(self.selected_species[self.current_index])
        self.magic = self.magic[self.current_index]
        self.using_magic.set(self.magic)
        self.flying = self.flying[self.current_index]
        self.is_flying.set(self.flying)
        self.index_label.delete(1.0, tk.END)
        self.index_label.insert(1.0, self.current_index)
        self.update_image()

    def save_legacy(self):
        self.magic[self.current_index] = self.magic
        self.flying[self.current_index] = self.flying
        species = self.species_var.get()
        print(species)
        self.selected_species[self.current_index] = species
        settings = {"images":self.images, "magic":self.magic, "flying":self.flying, "pony_count":self.pony_count, "unicorn_count":self.unicorn_count, "pegasus_count":self.pegasus_count, "selected_species":self.selected_species}
        with open(self.json_file, "w") as f:
            json.dump(settings, f)
        print("json created: ", f)

def create_json(root_directory, json_path):
    data = []
    with open(json_path, "w") as file:
        for f in os.listdir(root_directory):
            if f.endswith('.png') == True or f.endswith('.jpeg') == True or f.endswith('.jpg') == True:
                entry = {"images":f, "magic":False, "flying":False, "pony_count":0, "unicorn_count":0, "pegasus_count":0, "selected_species":0}
                data.append(entry)
        json.dump(data, file, indent=4)
    print("json created: ", json_path)

def load_legacy(json_path, new_json):
    with open(json_path, 'r') as file:
        data = json.load(file)
        magic = data["magic"]
        flying = data["flying"]
        pony_count = data["pony_count"]
        unicorn_count = data["unicorn_count"]
        pegasus_count = data["pegasus_count"]
        selected_species = data["selected_species"]
        images = data["images"]
    restructured = []
    i = 0
    for x in range(len(images)):
        entry = {"images":images[i], "magic":magic[i], "flying":flying[i], "pony_count":pony_count[i], "unicorn_count":unicorn_count[i], "pegasus_count":pegasus_count[i], "selected_species":selected_species[i]}
        restructured.append(entry)
        i += 1
    with open(new_json, "w") as f:
        json.dump(restructured, f, indent=4)
    print("json converted: ", new_json)


if __name__ == "__main__":
    print("Select image directory")
    root_directory = filedialog.askdirectory()
    ask_save = input("Would you like to create a .json file? (yes/no): ")
    if ask_save.lower() == 'yes':
        print("Save json path")
        json_file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        create_json(root_directory, json_file)
    elif ask_save.lower() == 'legacy':
        print("Selected import json")
        json_file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        print("Enter new filename")
        new_json = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        load_legacy(json_file, new_json)
        json_file = new_json
    else:
        print("Load json path")
        json_file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    app = ImageViewer(root_directory, json_file)
    app.mainloop()
