# PDF-Breaker

**PDF OCR and Unlock Tool** - Extract text from PDFs using OCR or remove passwords via manual entry or brute force.

## Requirements

- Python 3.12.6 or higher
- Required Python packages:
  - `pytesseract`
  - `pdf2image`
  - `pikepdf`
  - `Pillow` (for image processing)

  You can install the required packages using the following command:
  ```bash
  pip install pytesseract pdf2image pikepdf Pillow
Features
OCR (Optical Character Recognition): Extracts text from PDFs by converting PDF pages into images and then using OCR to read the text.
Unlock PDF with Password: Allows you to unlock password-protected PDFs by entering the password manually.
Brute Force PDF Unlocking: Attempts to unlock password-protected PDFs by trying all combinations of passwords (using letters and numbers).
Usage
Select PDF File: Choose the PDF file you want to work with.
Set Export Path: Choose the folder where you want the output to be saved.
Choose OCR or Unlock Options:
Use OCR to extract text from the PDF.
Use the Unlock PDF with Password option if you know the password.
Use the Brute Force Unlock option to try multiple password combinations automatically.
How to Run the Application
Clone or download the repository.
Install the required dependencies using the following:
bash
Másolás
Szerkesztés
pip install -r requirements.txt
Run the application using Python:
bash
Másolás
Szerkesztés
python app-test.py
This will open the application window where you can interact with the tool.
Interface Overview
The application consists of two main tabs:

OCR Tab: Extracts text from a PDF using OCR. You can select a PDF, specify the export path, and start the OCR process.
Unlock PDF Tab: Allows you to either enter a password to unlock a PDF manually or attempt to brute force the password.
License
This project is licensed under the MIT License.

Disclaimer
This tool is intended for legal and ethical purposes only. Ensure that you have permission to manipulate any PDFs you are working with.

markdown
Másolás
Szerkesztés

This markdown file includes:

1. **Project Title and Description**
2. **Requirements** for Python and dependencies
3. **Features** of the application
4. **How to use the tool** and run it
5. **Interface Overview**
6. **License Information**
7. **Disclaimer**

Let me know if you'd like any additional information!