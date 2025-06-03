import tkinter as tk
from tkinter import filedialog, ttk
import threading
import time
import pytesseract
from pdf2image import convert_from_path
import os
import pikepdf
import itertools
import string

class PDFProcessor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Processing Application")
        self.root.geometry("600x500")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.ocr_tab = ttk.Frame(self.notebook)
        self.unlock_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.ocr_tab, text="OCR")
        self.notebook.add(self.unlock_tab, text="Unlock PDF")
        
        # Initialize UI elements
        self.setup_ocr_tab()
        self.setup_unlock_tab()
        
        # Status and progress elements
        self.progress_bar = ttk.Progressbar(self.root, mode="indeterminate")
        self.progress_bar.pack(pady=10, fill=tk.X)
        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack()

    def setup_ocr_tab(self):
        frame = tk.Frame(self.ocr_tab)
        frame.pack(pady=20)
        
        # File selection
        tk.Label(frame, text="Select PDF File:").grid(row=0, column=0, padx=5, pady=5)
        self.ocr_file_path = tk.Entry(frame, width=40)
        self.ocr_file_path.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame, text="Browse", command=lambda: self.select_file(self.ocr_file_path)).grid(row=0, column=2, padx=5, pady=5)
        
        # Export path
        tk.Label(frame, text="Export Path:").grid(row=1, column=0, padx=5, pady=5)
        self.ocr_export_path = tk.Entry(frame, width=40)
        self.ocr_export_path.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(frame, text="Browse", command=lambda: self.select_export_path(self.ocr_export_path)).grid(row=1, column=2, padx=5, pady=5)
        
        # Process button
        tk.Button(self.ocr_tab, text="Start OCR", command=self.process_pdf).pack(pady=10)

    def setup_unlock_tab(self):
        frame = tk.Frame(self.unlock_tab)
        frame.pack(pady=20)
        
        # File selection
        tk.Label(frame, text="Select PDF File:").grid(row=0, column=0, padx=5, pady=5)
        self.unlock_file_path = tk.Entry(frame, width=40)
        self.unlock_file_path.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame, text="Browse", command=lambda: self.select_file(self.unlock_file_path)).grid(row=0, column=2, padx=5, pady=5)
        
        # Export path
        tk.Label(frame, text="Export Path:").grid(row=1, column=0, padx=5, pady=5)
        self.unlock_export_path = tk.Entry(frame, width=40)
        self.unlock_export_path.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(frame, text="Browse", command=lambda: self.select_export_path(self.unlock_export_path)).grid(row=1, column=2, padx=5, pady=5)
        
        # Password entry
        tk.Label(frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(frame, width=40, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.unlock_tab)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Unlock with Password", command=self.unlock_pdf_with_password).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Brute Force Unlock", command=self.brute_force_pdf).pack(side=tk.LEFT, padx=5)

    def select_file(self, entry_widget):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)

    def select_export_path(self, entry_widget):
        export_path = filedialog.askdirectory()
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, export_path)

    def process_pdf(self):
        def run_task():
            self.progress_bar.start()
            pdf_path = self.ocr_file_path.get()
            export_path = self.ocr_export_path.get()
            
            if not pdf_path or not export_path:
                self.status_label.config(text="Please select a file and export path!")
                self.progress_bar.stop()
                return
            
            try:
                # Convert PDF to images
                images = convert_from_path(pdf_path)
                extracted_text = ""
                
                # Process each page
                for i, img in enumerate(images):
                    extracted_text += f"Page {i+1}:\n{pytesseract.image_to_string(img)}\n"
                    extracted_text += "=" * 50 + "\n"
                
                # Save extracted text
                output_file = os.path.join(export_path, "extracted_text.txt")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(extracted_text)
                
                self.status_label.config(text=f"Process completed! Saved to {output_file}")
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}")
            finally:
                self.progress_bar.stop()
        
        self.status_label.config(text="Processing...")
        threading.Thread(target=run_task).start()

    def unlock_pdf_with_password(self):
        def run_task():
            self.progress_bar.start()
            pdf_path = self.unlock_file_path.get()
            password = self.password_entry.get()
            export_path = self.unlock_export_path.get()
            
            if not pdf_path or not export_path or not password:
                self.status_label.config(text="Please select a file, export path, and provide a password!")
                self.progress_bar.stop()
                return
            
            try:
                # Attempt to open the PDF with the provided password
                pdf = pikepdf.open(pdf_path, password=password)
                unlocked_pdf_path = os.path.join(export_path, "unlocked.pdf")
                pdf.save(unlocked_pdf_path)
                self.status_label.config(text=f"PDF unlocked and saved to {unlocked_pdf_path}")
            except pikepdf.PasswordError:
                self.status_label.config(text="Incorrect password!")
            except Exception as e:
                self.status_label.config(text=f"An error occurred: {str(e)}")
            finally:
                self.progress_bar.stop()
        
        self.status_label.config(text="Unlocking PDF...")
        threading.Thread(target=run_task).start()

    def brute_force_pdf(self):
        def run_task():
            self.progress_bar.start()
            pdf_path = self.unlock_file_path.get()
            export_path = self.unlock_export_path.get()
            
            if not pdf_path or not export_path:
                self.status_label.config(text="Please select a file and export path!")
                self.progress_bar.stop()
                return
            
            # Bruteforce all possible password combinations
            characters = string.ascii_letters + string.digits
            found = False
            
            try:
                for length in range(1, 5):  # Try passwords of length 1 to 4
                    for password_tuple in itertools.product(characters, repeat=length):
                        password = ''.join(password_tuple)
                        try:
                            # Attempt to open the PDF with the generated password
                            pdf = pikepdf.open(pdf_path, password=password)
                            unlocked_pdf_path = os.path.join(export_path, "unlocked.pdf")
                            pdf.save(unlocked_pdf_path)
                            self.status_label.config(text=f"PDF unlocked with password '{password}' and saved to {unlocked_pdf_path}")
                            found = True
                            break
                        except pikepdf.PasswordError:
                            continue
                    if found:
                        break
                
                if not found:
                    self.status_label.config(text="Failed to unlock PDF with brute force.")
            except Exception as e:
                self.status_label.config(text=f"An error occurred: {str(e)}")
            finally:
                self.progress_bar.stop()
        
        self.status_label.config(text="Starting brute force...")
        threading.Thread(target=run_task).start()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PDFProcessor()
    app.run() 