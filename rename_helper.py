import os
import sys
import tkinter as tk
from tkinter import messagebox
from pdf2image import convert_from_path
from PIL import Image, ImageTk
import filename_proposer
import argparse

def pdf_preview(pdf_path, output_path):
    images = convert_from_path(pdf_path)
    first_page_image = images[0]
    #first_page_image.save(output_path)
    return first_page_image

def rename_file(folder_path,old_filename,new_filename):
    print("Renaming ",old_filename,"to",new_filename)
    old_file = os.path.join(folder_path,old_filename)
    new_file = os.path.join(folder_path,new_filename)
    os.rename(old_file,new_file)

def display_preview(image, file_name,folder_path, proposed_filename, max_width=800, max_height=800):
    def close():
        window.destroy()
    
    def yes():
        rename_file(folder_path,file_name,proposed_filename)
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
    parser = argparse.ArgumentParser(description="A script for renaming research papers with the scheme YEAR-AUTHOR-TITLE.pdf ")
    parser.add_argument("-f","--folder", type=str, help="Folder path that contains pdf files.",required=True)
    parser.add_argument("--auto_rename",help="Automatically rename without user confirmation. Be careful!",action="store_true")

    args = parser.parse_args()

    folder_path = args.folder

    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf") and not filename_proposer.is_valid_filename(file):
            file_path = os.path.join(folder_path, file)
            proposed_filename = filename_proposer.get_proposal(file_path,verbose=False)
            if proposed_filename:
                if args.auto_rename:
                    rename_file(folder_path,file,proposed_filename)
                else:
                    print(f"Previewing first page of {file}")
                    output_path = os.path.join(folder_path, f"{os.path.splitext(file)[0]}_preview.jpg")
                    preview_image = pdf_preview(file_path, output_path)
                    display_preview(preview_image, file, folder_path, proposed_filename)
            else:
                print("Error: Could not find proposal for ",file_path)

