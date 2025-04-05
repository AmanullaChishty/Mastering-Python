# pdf_editor/utils.py

from PIL import ImageTk

def pil_to_tkinter(pil_image):
    """Converts a PIL Image object to a Tkinter PhotoImage object."""
    if pil_image:
        return ImageTk.PhotoImage(pil_image)
    return None