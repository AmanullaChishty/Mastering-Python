# pdf_editor/gui.py
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
from .pdf_handler import PDFHandler,PDFHandlerError
from .utils import pil_to_tkinter
import os 

DEFAULT_ZOOM = 1.0
ZOOM_INCREMENT = 0.2

class PDFEditorApp:
    def __init__(self,root):
        self.root = root
        self.root.title("RUD PDF Editor")
        self.root.geometry("800x700")

        self.pdf_handler = PDFHandler()
        self.current_page_num =0
        self.total_pages = 0
        self.tk_image = None 
        self.current_zoom = DEFAULT_ZOOM

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_menu()
        self.create_toolbar()
        self.create_viewer()
        self.create_statusbar()

        self.update_ui_state()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar,tearoff=0)
        menubar.add_cascade(label="File",menu=file_menu)
        file_menu.add_command(label="Open PDF...",command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(lebel="Merge PDFs...",command=self.prompt_merge_pdfs)
        file_menu.add_separator()
        file_menu.add_command(label="Exit",command=self.root.quit)

        edit_menu =tk.Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        self.remove_pwd_menu_idx = edit_menu.add_command(label="Remove Password...",command=self.prompt_remove_password, state=tk.DISABLED)
        self.extract_page_menu_idx = edit_menu.add_command(label="Extract Current Page...", command=self.prompt_extract_page, state=tk.DISABLED)
    
    def create_toolbar(self):
        toolbar = ttk.Frame(self.main_frame,relief=tk.RAISED,borderwidth=1)
        toolbar.pack(side=tk.TOP,fill=tk.X,pady=2)

        # Open Button
        open_btn = ttk.Button(toolbar,text="Open",command=self.open_file)
        open_btn.pack(side=tk.LEFT,padx=5,pady=2)

        # Merge Button
        merge_btn = ttk.Button(toolbar,text='Merge', command=self.promp_merge_pdfs)
        merge_btn.pack(side=tk.LEFT, padx=5,pady=2)

        # Separator
        ttk.Separator(toolbar,orient=tk.VERTICAL).pack(side=tk.LEFT,fill=tk.Y, padx=10, pady=2)

        # Navigation and Page Info
        self.prev_btn = ttk.Button(toolbar, text="< Prev",command=self.prev_page, state=tk.DISABLED)
        self.prev_btn.pack(side=tk.LEFT, padx=5,pady=2)

        self.page_label_var = tk.StringVar(value="Page: - / -")
        page_label = ttk.Label(toolbar, textvariable=self.page_label_var, width=12,anchor=tk.CENTER)
        page_label.pack(side=tk.LEFT, padx=5, pady=2)

        self.next_btn = ttk.Button(toolbar,text="Next >", command=self.next_page, state=tk.DISABLED)
        self.next_btn.pack(side=tk.LEFT, padx=5, pady=2)

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill =tk.Y, padx=10, pady=2)
        zoom_in_btn = ttk.Button(toolbar, text="Zoom +", command=self.zoom_in, state=tk.DISABLED)
        zoom_in_btn.pack(side=tk.LEFT,padx=2,pady=2)
        zoom_out_btn = ttk.Button(toolbar,text="Zoom -", command=self.zoom_out, state=tk.DISABLED)
        zoom_out_btn.pack(side=tk.LEFT,padx=2,pady=2)
        self.zoom_in_btn = zoom_in_btn
        self.zoom_out_btn = zoom_out_btn