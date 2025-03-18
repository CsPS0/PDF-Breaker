import pytesseract
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

poppler_path = r"C:\poppler-24.08.0\Library\bin"
images = convert_from_path("linux_docker_unlocked.pdf", poppler_path=poppler_path)

output_file = "extracted_text.txt"

with open(output_file, "w", encoding="utf-8") as f:
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        f.write(f"Page {i+1}:\n{text}\n")
        f.write("=" * 50 + "\n")

print(f"Szöveg sikeresen mentve: {output_file}")