import tkinter as tk
from tkinter import filedialog, ttk
import threading
import time
import pytesseract
from pdf2image import convert_from_path
import os

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

root = tk.Tk()
root.title("PDF OCR Application")
root.geometry("500x300")

frame = tk.Frame(root)
frame.pack(pady=20)

tl_file = tk.Label(frame, text="Select PDF File:")
tl_file.grid(row=0, column=0, padx=5, pady=5)
entry_file_path = tk.Entry(frame, width=40)
entry_file_path.grid(row=0, column=1, padx=5, pady=5)
btn_file = tk.Button(frame, text="Browse", command=select_file)
btn_file.grid(row=0, column=2, padx=5, pady=5)

tl_export = tk.Label(frame, text="Export Path:")
tl_export.grid(row=1, column=0, padx=5, pady=5)
entry_export_path = tk.Entry(frame, width=40)
entry_export_path.grid(row=1, column=1, padx=5, pady=5)
btn_export = tk.Button(frame, text="Browse", command=select_export_path)
btn_export.grid(row=1, column=2, padx=5, pady=5)

btn_process = tk.Button(root, text="Start OCR", command=process_pdf)
btn_process.pack(pady=10)

progress_bar = ttk.Progressbar(root, mode="indeterminate")
progress_bar.pack(pady=10, fill=tk.X)

lbl_status = tk.Label(root, text="")
lbl_status.pack()

root.mainloop()
