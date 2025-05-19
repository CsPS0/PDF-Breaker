# PDF-Breaker

**PDF OCR and Unlock Tool**
Extract text from PDFs using OCR or remove passwords via manual entry or brute force.

## Requirements

- Python 3.12.6 or higher
- Required Python packages:
    - `pytesseract`
    - `pdf2image`
    - `pikepdf`
    - `Pillow` (for image processing)

Install the required packages with:

```bash
pip install pytesseract pdf2image pikepdf Pillow
```


## Features

- **OCR (Optical Character Recognition):**
Extract text from PDFs by converting pages to images and using OCR to read the text.
- **Unlock PDF with Password:**
Unlock password-protected PDFs by entering the password manually.
- **Brute Force PDF Unlocking:**
Attempt to unlock password-protected PDFs by trying combinations of letters and numbers.


## Usage

1. **Select PDF File:**
Choose the PDF you want to process.
2. **Set Export Path:**
Choose the folder where output files will be saved.
3. **Choose an Option:**
    - Use **OCR** to extract text from the PDF.
    - Use **Unlock PDF with Password** if you know the password.
    - Use **Brute Force Unlock** to try multiple password combinations automatically.

## How to Run the Application

1. Clone or download this repository.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app-test.py
```

This will open the application window where you can interact with the tool.

## Interface Overview

The application has two main tabs:

- **OCR Tab:**
Extract text from a PDF using OCR. Select a PDF, specify the export path, and start the OCR process.
- **Unlock PDF Tab:**
Enter a password to unlock a PDF manually or attempt to brute force the password.


## License

This project is licensed under the MIT License.

## Disclaimer

This tool is intended for legal and ethical purposes only. Ensure you have permission to manipulate any PDFs you are working with.