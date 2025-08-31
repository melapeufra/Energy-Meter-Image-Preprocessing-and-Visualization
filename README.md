# Meter Conso → Excel (OCR)

Extract electricity meter readings from photos (e.g., XS212 / Siconia) and export them to Excel.

> The script reads the **register** (e.g. `1.8.2`), the **numeric value** (e.g. `000522.580`), and the **unit** (`kWh`).

---

## Features
- Works on a single image or a whole folder
- Detects and flattens the LCD screen region
- OCR tuned with digit/letter whitelists
- Writes a timestamped **Excel** file
- Saves debug crops for quick visual checks

---

## Requirements
- Python **3.9+**
- **Tesseract OCR** (v5+)
- Python packages:
  ```bash
  pip install opencv-python pillow pytesseract pandas openpyxl
  ```

### Install Tesseract
- **macOS**
  ```bash
  brew install tesseract
  ```
- **Ubuntu/Debian**
  ```bash
  sudo apt-get update
  sudo apt-get install tesseract-ocr
  ```
- **Windows**  
  If Tesseract isn’t on PATH, set it in the script:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
  ```

---

## Quick Start
1. Put your photos in the `images/` folder **or** set `INPUT_PATH` at the top of `meter_conso_to_excel.py`.
2. Run:
   ```bash
   python meter_conso_to_excel.py
   ```
3. Open the Excel created in `output/` (example: `meter_readings_YYYYMMDD_HHMMSS.xlsx`).

---

## Output
### Excel columns
| Column     | Description                                      |
|------------|--------------------------------------------------|
| `file`     | Source image filename                            |
| `register` | e.g. `1.8.2`                                     |
| `reading`  | e.g. `000522.580` (commas normalized to dots)    |
| `unit`     | Typically `kWh`                                  |
| `raw_ocr`  | Unparsed OCR text (for debugging)                |

### Debug images
Saved under `output/meter_debug_<timestamp>/`:
- `_display.png` — detected LCD area (after perspective fix)
- Intermediate binarizations and `digit.png` per-digit crops

---

## Project Structure
```
.
├─ meter_conso_to_excel.py
├─ images/              # your photos
└─ output/              # Excel + debug crops (auto-created)
```

---

## Tips
- If Excel is open, close it before re-running (files are timestamped to avoid conflicts).
- If your meter always shows **3 decimals**, you can force the decimal point when parsing.
- If the LCD isn’t detected correctly, adjust thresholds in `find_display_roi()` inside the script.

---

## License
This project is released under the **MIT License**. See the `LICENSE` file.
