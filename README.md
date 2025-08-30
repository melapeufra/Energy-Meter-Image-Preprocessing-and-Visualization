# Meter Conso → Excel (OCR)

Extract electricity meter readings from photos (e.g., XS212/Siconia) and export them to Excel.

> Reads the **register** (e.g. `1.8.2`), the **numeric value** (e.g. `000522.580`), and the **unit** (`kWh`).

---

## Features
- Works on a single image or a whole folder
- Detects and flattens the LCD screen region
- OCR with digit/letter whitelists tuned for meters
- Exports results to a timestamped Excel file
- Saves debug crops for quick visual checks

---

## Requirements
- Python 3.9+
- Tesseract OCR (v5+)
- Python packages:
  ```bash
  pip install opencv-python pillow pytesseract pandas openpyxl
macOS:
brew install tesseract
Windows (if Tesseract isn’t on PATH), set in the script:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

Quick Start

Put your images in the images/ folder or set INPUT_PATH in meter_conso_to_excel.py.

Run:
python meter_conso_to_excel.py
Open the Excel created in output/ (e.g. meter_readings_YYYYMMDD_HHMMSS.xlsx).

Output

Excel columns

file – source image filename

register – e.g. 1.8.2

reading – e.g. 000522.580 (commas normalized to dots)

unit – typically kWh

raw_ocr – raw text (for debugging)

Debug images

Saved in output/meter_debug_<timestamp>/:

_display.png (detected LCD)

intermediate binarizations and per-digit crops

Project Structure
.
├─ meter_conso_to_excel.py
├─ images/              # your photos
└─ output/              # Excel + debug crops (auto-created)

Tips

If Excel is open, close it before re-running (files are timestamped to avoid conflicts).
For meters with fixed 3 decimals, you can force the decimal point in parsing.
If the LCD isn’t detected correctly, adjust thresholds in find_display_roi().

License
MIT License

Copyright (c) 2025 Your Name or Organization

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
