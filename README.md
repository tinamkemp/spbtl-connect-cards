# SPBTL Connect Cards

Print-ready connect card generator for **St. Paul's by-the-Lake**, Chicago.

Produces a 2-page letter-size PDF — 4 cards per page (2×2), designed for duplex printing on cardstock and two cuts.

## Output

- **Page 1 (front):** Church header, contact fields (name, email, phone with mobile/landline, address), "I am a" checkboxes, privacy notice
- **Page 2 (back):** Interests checkboxes, prayer request with write-in lines, "How did you hear" checkboxes, privacy notice

## Requirements

- Python 3.8+
- [ReportLab](https://pypi.org/project/reportlab/)

```bash
pip install reportlab
```

## Usage

1. Place `logo.png` (the church shield) in the same directory as `make_cards.py`.
2. Run the script:

```bash
python make_cards.py
```

3. Output: `SPBTL_Connect_Cards.pdf` in the current directory.

## Printing — Epson ET-16650

1. **Paper:** Letter-size cardstock, 65–80 lb cover. Load in the **rear feed slot** (not front cassette) one sheet at a time.
2. **Media type:** Set to **Thick Paper** or **Cardstock** in the printer driver.
3. **Page 1 first:** Print with two-sided printing **off**. Select page 1 only.
4. **Flip on short edge:** Flip the stack top-to-bottom (not left-to-right) and reload.
5. **Page 2:** Print page 2 only.

## Cutting

Two cuts produce 4 cards per sheet — no crop marks needed:

| Cut | Direction | Position |
| --- | --- | --- |
| 1 | Horizontal | 5.5" from top |
| 2 | Vertical | 4.25" from left |

Cards have 0.25" inner padding, so cuts can be 1–2 mm off without affecting the content area.

## Customization

All content is in `make_cards.py`. The most common changes:

- **Checkbox options:** Edit the lists passed to `cbline()` in `draw_front()` and `draw_back()`
- **Font:** Add your Garamond `.ttf` paths to the front of each list in `FONT_CANDIDATES`
- **Spacing / font sizes:** Adjust `gap=` and `fs=` arguments on each element
- **Church info:** Edit the strings in the header block of `draw_front()`

## Files

| File | Purpose |
| --- | --- |
| `make_cards.py` | PDF generator — edit this to change content or layout |
| `logo.png` | Church shield logo (not committed — add your own copy) |
| `SPBTL_Connect_Cards.pdf` | Generated output (not committed) |

## Notes

- The PDF uses Times New Roman on macOS and Windows, and Liberation Serif (its open-source equivalent) on Linux. The script finds the font automatically. To use Garamond, install the font and add it to `FONT_CANDIDATES`.
- Word and Google Docs versions of the card exist for content review only — always print from the PDF.
- See the *Connect Card — Printing & File Reference* doc in the SPBTL shared Google Drive for full printing and editing instructions.
