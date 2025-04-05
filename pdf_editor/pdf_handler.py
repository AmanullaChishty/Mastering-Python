# pdf_editor/pdf_handler.py

import pypdf
import fitz
import io
from PIL import Image
import pypdf.errors

class PDFHandlerError(Exception):
    """Custom exception for PDF handling errors."""
    pass

class PDFHandler:
    """Handles all PDF manipulation tasks."""

    def __init__(self):
        self.current_doc = None
        self. current_filepath = None
    
    def open_pdf(self, filepath):
        """Opens a PDF file using PyMuPDF for viewing."""
        try:
            self.current_doc = fitz.open(filepath)
            self.current_filepath = filepath
            if self.current_doc.is_encrypted and not self.current_doc.authenticate(''):
                # If encrypted and needs a password (empty '' fails)
                # We will handle password entry during viewing or operations
                pass # Or raise an exception if immediate auth is needed
            return self.current_doc.page_count
        except Exception as e:
            self.current_doc = None
            self.current_filepath = None
            raise PDFHandlerError(f"Failed to opne PDF: {e}")
    
    def get_page_image(self,page_number,zoom=1.0):
        """Renders a specific page as a PIL Image."""
        if not self.current_doc:
            raise PDFHandlerError("No PDF document is currently open.")
        if not 0 <= page_number<self.current_doc.page_count:
            raise PDFHandlerError(f"Invalid page number: {page_number+1}")
        
        try:
            page = self.current_doc.load_page(page_number)
            # Increase resolution by applying zoom
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix = mat)
            # Create image from pixmap data
            if pix.alpha:
                img = Image.frombytes("RGBA",[pix.width, pix.height], pix.samples)
            else:
                img = Image.frombytes("RGB",[pix.width,pix.height], pix.samples)
            return img
        except Exception as e:
            raise PDFHandlerError(f"Failed to render page {page_number + 1}: {e}")
        
    def needs_password(self, filepath=None):
        """Checks if the currently loaded PDF or a specific file needs a password."""
        path_to_check = filepath if filepath else self.current_filepath
        if not path_to_check:
            return False # No file loaded or specified

        try:
            # Use pypdf for a quick encrytion check
            reader = pypdf.PdfReader(path_to_check,strict=False) # Use strict=False for broader compatibility
            return reader.is_encrypted
        except Exception:
            # Could fail if file doesn't exist or is corrupt, treat as not needing password here
            # More specific error handling could be added
             return False # Assume not encrypted if check fails
    
    def remove_password(self, input_path, output_path, password):
        """Removes password from a PDF file."""
        try:
            reader = pypdf.PdfReader(input_path)
            if not reader.is_encrypted:
                raise PDFHandlerError("PDF is not encrypted.")
            
            if reader.decrypt(password) == pypdf.PasswordType.NOT_DECRYPTED:
                raise PDFHandlerError("Incorrect password provided.")
            
            writer = pypdf.PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            
            with open(output_path,"wb") as f_out:
                writer.write(f_out)
            return True
        except pypdf.errors.PdfReadError as e:
            raise PDFHandlerError(f"Error reading PDF: {e}. Is the password correct?")
        except Exception as e:
            raise PDFHandlerError(f"Failed to remove password: {e}")
    
    def merge_pdfs(self, input_paths, output_path):
        """Merges multiple PDF files into one."""
        if not input_paths or len(input_paths)<2:
            raise PDFHandlerError("Please select at least two PDF files to merge.")
        
        merger = pypdf.PdfMerger(strict=False) # Use strict=False for broader compatibility
        try:
            for pdf_path in input_paths:
                reader_check = pypdf.PdfReader(pdf_path,strict=False)
                if reader_check.is_encrypted:
                    raise PDFHandlerError(f"Cannot merge encrypted PDF: {pdf_path}. Please decrypt it first.")
                merger.append(pdf_path)
            
            with open(output_path,"wb") as f_out:
                merger.write(f_out)
            merger.close()
            return True
        except Exception as e:
            merger.close() # Ensure files are closed even on error
            raise PDFHandlerError(f"Failed to merge PDFs: {e}")
    
    def extract_page(self, input_path, output_path, page_number_to_extract):
        """Extracts a specific page (1-based index) from a PDF."""
        try:
            reader = pypdf.PdfReader(input_path)

            if reader.is_encrypted:
                raise PDFHandlerError(f"Cannot extract from encrypted PDF: {input_path}. Please decrypt it first.")
            
            total_pages = len(reader.pages)
            if not 1<= page_number_to_extract <= total_pages:
                raise PDFHandlerError(f"Invalid page number: {page_number_to_extract}. PDF has {total_pages} pages.")
            
            writer = pypdf.PdfWriter()
            writer.add_page(reader.pages[page_number_to_extract-1])

            with open(output_path,"wb") as f_out:
                writer.write(f_out)
            return True
        except Exception as e:
            raise PDFHandlerError(f"Failed to extract page: {e}")
        
    def cloase_pdf(self):
        """Closes the currently open PyMuPDF document."""
        if self.current_doc:
            self.current_doc.close()
            self.current_doc= None
            self.current_filepath = None