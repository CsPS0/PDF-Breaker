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

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)

def select_export_path():
    export_path = filedialog.askdirectory()
    entry_export_path.delete(0, tk.END)
    entry_export_path.insert(0, export_path)

def process_pdf():
    def run_task():
        progress_bar.start()
        pdf_path = entry_file_path.get()
        export_path = entry_export_path.get()
        if not pdf_path or not export_path:
            lbl_status.config(text="Please select a file and export path!")
            progress_bar.stop()
            return
        
        images = convert_from_path(pdf_path)
        extracted_text = ""
        for i, img in enumerate(images):
            extracted_text += pytesseract.image_to_string(img) + "\n\n"
        
        output_file = os.path.join(export_path, "extracted_text.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(extracted_text)
        
        progress_bar.stop()
        lbl_status.config(text=f"Process completed! Saved to {output_file}")
    
    lbl_status.config(text="Processing...")
    thread = threading.Thread(target=run_task)
    thread.start()

def unlock_pdf_with_password():
    def run_task():
        progress_bar.start()
        pdf_path = entry_file_path.get()
        password = entry_password.get()
        export_path = entry_export_path.get()
        
        if not pdf_path or not export_path or not password:
            lbl_status.config(text="Please select a file, export path, and provide a password!")
            progress_bar.stop()
            return
        
        try:
            # Attempt to open the PDF with the provided password
            pdf = pikepdf.open(pdf_path, password=password)
            unlocked_pdf_path = os.path.join(export_path, "unlocked.pdf")
            pdf.save(unlocked_pdf_path)
            lbl_status.config(text=f"PDF unlocked and saved to {unlocked_pdf_path}")
        except pikepdf.PasswordError:  # Catch PasswordError directly
            lbl_status.config(text="Incorrect password!")
        except Exception as e:
            lbl_status.config(text=f"An error occurred: {e}")
        finally:
            progress_bar.stop()
    
    lbl_status.config(text="Unlocking PDF...")
    thread = threading.Thread(target=run_task)
    thread.start()

def brute_force_pdf():
    def run_task():
        progress_bar.start()
        pdf_path = entry_file_path.get()
        export_path = entry_export_path.get()
        
        if not pdf_path or not export_path:
            lbl_status.config(text="Please select a file and export path!")
            progress_bar.stop()
            return
        
        # Bruteforce all possible password combinations
        characters = string.ascii_letters + string.digits  # Define the characters for brute force
        found = False
        
        for length in range(1, 5):  # Try passwords of length 1 to 4 (adjust length as needed)
            for password_tuple in itertools.product(characters, repeat=length):
                password = ''.join(password_tuple)
                try:
                    # Attempt to open the PDF with the generated password
                    pdf = pikepdf.open(pdf_path, password=password)
                    unlocked_pdf_path = os.path.join(export_path, "unlocked.pdf")
                    pdf.save(unlocked_pdf_path)
                    lbl_status.config(text=f"PDF unlocked with password '{password}' and saved to {unlocked_pdf_path}")
                    found = True
                    break
                except pikepdf.PasswordError:
                    continue
            if found:
                break
        
        if not found:
            lbl_status.config(text="Failed to unlock PDF with brute force.")
        
        progress_bar.stop()
    
    lbl_status.config(text="Starting brute force...")
    thread = threading.Thread(target=run_task)
    thread.start()

# Create the main window
root = tk.Tk()
root.title("PDF OCR and Unlock Application")
root.geometry("500x400")

# Create notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# OCR Tab
tab_ocr = ttk.Frame(notebook)
notebook.add(tab_ocr, text="OCR")

# OCR Tab contents
frame_ocr = tk.Frame(tab_ocr)
frame_ocr.pack(pady=20)

tl_file = tk.Label(frame_ocr, text="Select PDF File:")
tl_file.grid(row=0, column=0, padx=5, pady=5)
entry_file_path = tk.Entry(frame_ocr, width=40)
entry_file_path.grid(row=0, column=1, padx=5, pady=5)
btn_file = tk.Button(frame_ocr, text="Browse", command=select_file)
btn_file.grid(row=0, column=2, padx=5, pady=5)

tl_export = tk.Label(frame_ocr, text="Export Path:")
tl_export.grid(row=1, column=0, padx=5, pady=5)
entry_export_path = tk.Entry(frame_ocr, width=40)
entry_export_path.grid(row=1, column=1, padx=5, pady=5)
btn_export = tk.Button(frame_ocr, text="Browse", command=select_export_path)
btn_export.grid(row=1, column=2, padx=5, pady=5)

btn_process = tk.Button(tab_ocr, text="Start OCR", command=process_pdf)
btn_process.pack(pady=10)

progress_bar = ttk.Progressbar(tab_ocr, mode="indeterminate")
progress_bar.pack(pady=10, fill=tk.X)

lbl_status = tk.Label(tab_ocr, text="")
lbl_status.pack()

# Unlock Tab
tab_unlock = ttk.Frame(notebook)
notebook.add(tab_unlock, text="Unlock PDF")

# Unlock Tab contents
frame_unlock = tk.Frame(tab_unlock)
frame_unlock.pack(pady=20)

tl_file_unlock = tk.Label(frame_unlock, text="Select PDF File:")
tl_file_unlock.grid(row=0, column=0, padx=5, pady=5)
entry_file_path = tk.Entry(frame_unlock, width=40)
entry_file_path.grid(row=0, column=1, padx=5, pady=5)
btn_file_unlock = tk.Button(frame_unlock, text="Browse", command=select_file)
btn_file_unlock.grid(row=0, column=2, padx=5, pady=5)

tl_export_unlock = tk.Label(frame_unlock, text="Export Path:")
tl_export_unlock.grid(row=1, column=0, padx=5, pady=5)
entry_export_path = tk.Entry(frame_unlock, width=40)
entry_export_path.grid(row=1, column=1, padx=5, pady=5)
btn_export_unlock = tk.Button(frame_unlock, text="Browse", command=select_export_path)
btn_export_unlock.grid(row=1, column=2, padx=5, pady=5)

tl_password = tk.Label(frame_unlock, text="Enter Password (for removal):")
tl_password.grid(row=2, column=0, padx=5, pady=5)
entry_password = tk.Entry(frame_unlock, width=40, show="*")
entry_password.grid(row=2, column=1, padx=5, pady=5)

btn_unlock = tk.Button(tab_unlock, text="Unlock with Password", command=unlock_pdf_with_password)
btn_unlock.pack(pady=10)

btn_bruteforce = tk.Button(tab_unlock, text="Bruteforce Unlock", command=brute_force_pdf)
btn_bruteforce.pack(pady=10)

progress_bar_unlock = ttk.Progressbar(tab_unlock, mode="indeterminate")
progress_bar_unlock.pack(pady=10, fill=tk.X)

root.mainloop()