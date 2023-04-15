import os
import sys
import tkinter as tk
from tkinter import messagebox
from pdf2image import convert_from_path
from PIL import Image, ImageTk
import filename_proposer

def pdf_preview(pdf_path, output_path):
    images = convert_from_path(pdf_path)
    first_page_image = images[0]
    #first_page_image.save(output_path)
    return first_page_image

def display_preview(image, file_name,folder_path, proposed_filename, max_width=800, max_height=800):
    def close():
        window.destroy()
    
    def yes():
        print("Renaming ",file_name,"to",proposed_filename)
        old_file = os.path.join(folder_path,file_name)
        new_file = os.path.join(folder_path,proposed_filename)
        os.rename(old_file,new_file)
        close()

    def no():
        print("Skipping ",file_path)
        close()

    # Resize the image if it's too large
    width, height = image.size
    if width > max_width or height > max_height:
        new_size = (max_width, int(height * (max_width / width)))
        if new_size[1] > max_height:
            new_size = (int(width * (max_height / height)), max_height)
        image = image.resize(new_size, Image.ANTIALIAS)

    window = tk.Tk()
    window.title(file_name)
    window.protocol("WM_DELETE_WINDOW", close)

    button_frame = tk.Frame(window)
    button_frame.pack()

    yes_button = tk.Button(button_frame, text="Yes", command=yes)
    yes_button.pack(side=tk.LEFT)

    choose_label = tk.Label(button_frame, text="Rename to?:\n " + proposed_filename)
    choose_label.pack(side=tk.LEFT)

    no_button = tk.Button(button_frame, text="No", command=no)
    no_button.pack(side=tk.LEFT)

    image = ImageTk.PhotoImage(image)
    label = tk.Label(window, image=image)
    label.pack()

    window.mainloop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rename_helper.py [folder_path]")
        sys.exit(1)

    folder_path = sys.argv[1]

    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, file)
            print(f"Previewing first page of {file}")
            output_path = os.path.join(folder_path, f"{os.path.splitext(file)[0]}_preview.jpg")
            preview_image = pdf_preview(file_path, output_path)
            proposed_filename = filename_proposer.get_proposal(file_path,verbose=False)
            if proposed_filename:
                display_preview(preview_image, file, folder_path, proposed_filename)
            else:
                print("Error: Could not find proposal for ",file_path)

