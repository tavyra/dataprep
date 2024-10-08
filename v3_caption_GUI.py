import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk

def load_json_to_lists(json_file_path):
    folder_paths = []
    descriptions = []
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        folder_paths = data["folder_paths"]
        descriptions_list = data["descriptions_list"]
        return folder_paths, descriptions_list

def save_description(folder_paths, descriptions, json_file):
    data = {
        "folder_paths": folder_paths,
        "descriptions_list": descriptions
    }
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)


def load_descriptions(json_file):
    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            return json.load(file)
    else:
        return {}


def create_interface(folder_paths, json_file, description_list):
    root = tk.Tk()
    root.title("Image Viewer")
    current_index = 0
    total_folders = len(folder_paths)
    saved_text = tk.StringVar()


    def update_display():
        nonlocal current_index
        nonlocal description_entry
        current_folder = folder_paths[current_index]
        caption = description_list[current_index]
        print(current_folder)
        #content = file.read()
        description_entry.insert(tk.END, caption)
        images = []
        try:
            files = sorted(os.listdir(current_folder))
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(current_folder, file)
                    img = Image.open(img_path)
                    images.append((file, img))

        except Exception as e:
            print(f"Error loading images: {e}")
        if len(images) > 5: images = images[:5]

        # Position of the image on the canvas
        x = 0
        y = 0
        photo = []

        for idx, (file, img) in enumerate(images):
            img = img.resize((360, 240), Image.LANCZOS)
            photo += [ImageTk.PhotoImage(img)]
            canvas.image = photo
        i = 0
        for image in images:
            canvas.create_image(x, y, image=photo[i], anchor=tk.NW)
            y = round(i/3) * 260
            i += 1
            x = (i%3) * 380
        #canvas.create_image(380, 0, image=photo[1], anchor=tk.NW)
        #canvas.create_image(760, 0, image=photo[2], anchor=tk.NW)
        return description_list[current_index]

    def next_folder():
        nonlocal current_index
        current_index = (current_index + 1) % total_folders
        description_entry.delete(1.0, tk.END)
        update_display()

    def prev_folder():
        nonlocal current_index
        description_entry.delete(1.0, tk.END)
        current_index = (current_index - 1) % total_folders
        update_display()

    def edit_json_at_index():
        nonlocal current_index
        nonlocal json_file
        nonlocal description_entry
        new_caption = description_entry.get("1.0", 'end-1c')
        description_list[current_index] = new_caption
        save_description(folder_paths, description_list, json_file)




    # Create a frame to hold the images
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=10, pady=10)

    # Create a canvas to display the images
    canvas = tk.Canvas(frame, width=1120, height=600)
    canvas.pack(fill=tk.BOTH, expand=True)

    controls_frame = tk.Frame(frame)
    controls_frame.pack(side=tk.BOTTOM, fill=tk.Y)

    prev_button = tk.Button(controls_frame, text="Previous", command=prev_folder)
    prev_button.pack(fill=tk.X)

    next_button = tk.Button(controls_frame, text="Next", command=next_folder)
    next_button.pack(fill=tk.X)

    description_entry = tk.Text(controls_frame, width=100, height=5)
    description_entry.pack(fill=tk.X)

    save_button = tk.Button(controls_frame, text="Save Description", command=edit_json_at_index)
    save_button.pack(fill=tk.X)

    update_display()
    root.mainloop()

def main():
    directory = filedialog.askdirectory()  # Show the directory selection dialog
    if directory:
        folder_paths = []
        try:
            with os.scandir(directory) as it:
                for entry in it:
                    if entry.is_dir():
                        folder_paths.append(entry.path)
        except: print("Please select a directory")
    ask_load = input("Would you like to load a .json file? (yes/no): ")
    if ask_load.lower() == 'yes':
        json_file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        folder_paths, descriptions_list = load_json_to_lists(json_file)
        data = {
            "folder_paths": folder_paths,
            "descriptions_list": descriptions_list
        }
    else:
        json_file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not json_file:
            print("No JSON file selected.")
        i = 0
        descriptions = []
        for folder_path in folder_paths:
            descriptions += [""]
        save_description(folder_paths, descriptions, json_file)
    create_interface(folder_paths, json_file, descriptions_list)


if __name__ == "__main__":
    main()

