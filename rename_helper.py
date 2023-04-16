import os
import sys
import tkinter as tk
from tkinter import messagebox
from pdf2image import convert_from_path
from PIL import Image, ImageTk
import filename_proposer
import argparse

def pdf_preview(pdf_path):
    """
    Generate a preview of the first page of a PDF file as an image.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        PIL.Image: An image object representing the first page of the PDF.
    """
    images = convert_from_path(pdf_path)
    first_page_image = images[0]
    return first_page_image

def rename_file(folder_path,old_filename,new_filename):
    """
    Rename a file in the specified folder.

    Args:
        folder_path (str): The path to the folder containing the file to be renamed.
        old_filename (str): The current filename.
        new_filename (str): The new filename.

    Returns:
        None
    """
    old_file = os.path.join(folder_path,old_filename)
    new_file = os.path.join(folder_path,new_filename)
    if os.path.exists(new_file):
        print("Can not rename ",old_filename, " -> New filename already exists: ", new_file)
        return
    print("Renaming ",old_filename,"to",new_filename)
    os.rename(old_file,new_file)

def display_preview(image, file_name,folder_path, proposed_filename, max_width=800, max_height=800):
    """
    Display a preview of an image in a window with buttons to rename the file or skip it.

    Args:
        image (PIL.Image): The image to display in the window.
        file_name (str): The current filename of the image file.
        folder_path (str): The path to the folder containing the image file.
        proposed_filename (str): The proposed new filename for the image file.
        max_width (int, optional): The maximum width of the displayed image. Defaults to 800.
        max_height (int, optional): The maximum height of the displayed image. Defaults to 800.

    Returns:
        None
    """
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
            proposed_filename = filename_proposer.get_proposal(file_path)
            if proposed_filename:
                if args.auto_rename:
                    rename_file(folder_path,file,proposed_filename)
                else:
                    print(f"Previewing first page of {file}")
                    preview_image = pdf_preview(file_path)
                    display_preview(preview_image, file, folder_path, proposed_filename)
            else:
                print("Could not find proposal for ",file_path)
        else:
            print("Skipping",file)

