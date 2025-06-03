# PDF Processor

A comprehensive PDF processing application that combines OCR (Optical Character Recognition) and PDF unlocking capabilities in a user-friendly GUI interface.

## Features

- **OCR Processing**: Extract text from PDF files and save it to a text file
- **PDF Unlocking**: Remove password protection from PDF files
  - Manual password entry
  - Brute force password cracking (for simple passwords)

## Prerequisites

- Python 3.7 or higher
- Tesseract OCR engine
- Poppler (for PDF to image conversion)
- Required Python packages:
  ```bash
  pip install pikepdf>=8.11.2
  pip install pdf2image>=1.17.0
  pip install pytesseract>=0.3.10
  ```

### Installing Prerequisites

#### Windows:
1. Install Tesseract OCR:
   - Download the installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - Add Tesseract to your system PATH

2. Install Poppler:
   - Download from [poppler releases](http://blog.alivate.com.au/poppler-windows/)
   - Extract to a folder (e.g., C:\poppler-xx.xx.x)
   - Add the bin folder to your system PATH

#### Linux:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils
```

#### macOS:
```bash
brew install tesseract
brew install poppler
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/pdf-processor.git
cd pdf-processor
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

Alternatively, you can install the packages individually:
```bash
pip install pikepdf>=8.11.2
pip install pdf2image>=1.17.0
pip install pytesseract>=0.3.10
```

## Usage

1. Run the application:
```bash
python pdf_cracker/pdf_processor.py
```

2. The application has two main tabs:

### OCR Tab
- Click "Browse" to select a PDF file
- Choose an export directory
- Click "Start OCR" to begin text extraction
- The extracted text will be saved to a text file in the chosen directory

### Unlock PDF Tab
- Click "Browse" to select a password-protected PDF
- Choose an export directory
- Either:
  - Enter the known password and click "Unlock with Password"
  - Click "Brute Force Unlock" to attempt to crack the password

## Notes

- The brute force feature is limited to simple passwords (length 1-4 characters) by default
- For longer passwords, modify the `range(1, 5)` in the `brute_force_pdf` method
- OCR accuracy depends on the quality of the PDF and the Tesseract installation

## License

This project is licensed under the MIT License - see the LICENSE file for details.