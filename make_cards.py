"""
SPBTL Connect Cards — PDF Generator
St. Paul's by-the-Lake, Chicago

Generates a 2-page letter-size PDF:
  Page 1: Front side — 4 cards (2×2), contact info and "I am a" checkboxes
  Page 2: Back side — 4 cards (2×2), interests, prayer request, how did you hear

Print duplex, flip on SHORT EDGE, then make two cuts:
  Horizontal at 5.5" from top
  Vertical at 4.25" from left

Dependencies:
    pip install reportlab pillow

Usage:
    python make_cards.py
    # Output: SPBTL_Connect_Cards.pdf
"""

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
import os

# ── Fonts ─────────────────────────────────────────────────────────────────────
# Uses Times New Roman on macOS/Windows, or Liberation Serif (its open-source
# metric-compatible equivalent) on Linux. The first path that exists is used.
# To use Garamond instead, put your Garamond .ttf paths first in each list.
FONT_CANDIDATES = {
    "Serif": [
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",          # macOS
        "C:/Windows/Fonts/times.ttf",                                      # Windows
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",  # Linux
    ],
    "Serif-Bold": [
        "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
        "C:/Windows/Fonts/timesbd.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    ],
    "Serif-Italic": [
        "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
        "C:/Windows/Fonts/timesi.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    ],
}

for name, paths in FONT_CANDIDATES.items():
    path = next((p for p in paths if os.path.exists(p)), None)
    if path is None:
        raise FileNotFoundError(
            f"No font found for {name}. Tried:\n  " + "\n  ".join(paths) +
            "\nAdd a valid .ttf path to FONT_CANDIDATES in this script."
        )
    pdfmetrics.registerFont(TTFont(name, path))

# ── Logo ──────────────────────────────────────────────────────────────────────
# Place the church shield logo (PNG) in the same directory as this script,
# named 'logo.png'. It will be embedded at ~0.4" × 0.5" in the card header.
LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo.png")

# ── Page / card geometry ───────────────────────────────────────────────────────
PW, PH = letter          # 612 × 792 pt  (8.5" × 11")
MARGIN  = 0.25 * 72     # 18 pt page margin
CW = (PW - 2 * MARGIN) / 2   # card width  = 288 pt (4")
CH = (PH - 2 * MARGIN) / 2   # card height = 378 pt (5.25")
PAD = 18                      # inner card padding — 0.25" cut margin of error

# Card lower-left origins (ReportLab: y=0 at bottom of page)
ORIGINS = [
    (MARGIN,        MARGIN + CH),   # top-left
    (MARGIN + CW,   MARGIN + CH),   # top-right
    (MARGIN,        MARGIN),        # bottom-left
    (MARGIN + CW,   MARGIN),        # bottom-right
]

OUTPUT = "SPBTL_Connect_Cards.pdf"

# ── Helpers ───────────────────────────────────────────────────────────────────

def sc(text):
    """Small-caps simulation: uppercase the text."""
    return text.upper()

def rule(c, lx, y, rx, width=0.6):
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(width)
    c.line(lx, y, rx, y)

def underline(c, x1, x2, y, width=0.5):
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)

def checkbox(c, x, y, size=8):
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.7)
    c.rect(x, y, size, size, fill=0)

def field(c, label, lx, rx, y, fs_label=10.5, gap=16):
    """Draw a bold label + underline fill line. Returns new y."""
    c.setFont("Serif-Bold", fs_label)
    c.setFillColorRGB(0, 0, 0)
    lw = c.stringWidth(sc(label) + "  ", "Serif-Bold", fs_label)
    c.drawString(lx, y, sc(label))
    underline(c, lx + lw, rx, y - 1.5)
    return y - gap

def cbline(c, text, lx, y, fs=10, gap=13.5):
    """Draw a checkbox + label. Returns new y."""
    checkbox(c, lx, y - 1, size=8)
    c.setFont("Serif", fs)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(lx + 12, y, text)
    return y - gap

# ── FRONT card ────────────────────────────────────────────────────────────────

def draw_front(c, ox, oy):
    lx = ox + PAD
    rx = ox + CW - PAD
    y  = oy + CH - PAD

    # Logo + church name + tagline
    LOGO_H, LOGO_W = 34, 28
    logo_top = y
    if os.path.exists(LOGO_PATH):
        c.drawImage(LOGO_PATH, lx, logo_top - LOGO_H,
                    width=LOGO_W, height=LOGO_H,
                    mask='auto', preserveAspectRatio=True)
    tx = lx + LOGO_W + 5
    c.setFont("Serif-Bold", 13)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(tx, logo_top - 13, sc("St. Paul\u2019s by-the-Lake"))
    c.setFont("Serif-Bold", 7.5)
    c.drawString(tx, logo_top - 24, sc("The Episcopal Church in Rogers Park Since 1882"))

    y = logo_top - LOGO_H - 10
    c.setFont("Serif", 9)
    c.drawString(lx, y, "7100 N Ashland Blvd  \u2022  Chicago, IL 60626")
    y -= 10
    c.drawString(lx, y, "773-764-6514  \u2022  stpaulsbythelake.org")
    y -= 10
    rule(c, lx, y, rx, width=0.7)
    y -= 18

    # Connect heading
    c.setFont("Serif-Bold", 13)
    c.setFillColorRGB(0, 0, 0)
    cw_str = sc("Connect ")
    c.drawString(lx, y, cw_str)
    tw = c.stringWidth(cw_str, "Serif-Bold", 13)
    c.setFont("Serif", 11)
    c.drawString(lx + tw, y, "with St. Paul\u2019s by-the-Lake")
    y -= 12

    # Optional note
    c.setFont("Serif-Italic", 8.5)
    c.setFillColorRGB(0.33, 0.33, 0.33)
    c.drawString(lx, y, "Please share only what you\u2019re comfortable with\u2014no field is required.")
    c.setFillColorRGB(0, 0, 0)
    y -= 16

    # Contact fields
    y = field(c, "Name",          lx, rx, y)
    y = field(c, "Email",         lx, rx, y)

    # Phone with inline mobile/landline checkboxes
    c.setFont("Serif-Bold", 10.5)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(lx, y, sc("Phone"))
    plw = c.stringWidth(sc("Phone") + "  ", "Serif-Bold", 10.5)
    cbx = lx + plw + 1
    checkbox(c, cbx, y - 1, size=8)
    c.setFont("Serif", 9)
    c.drawString(cbx + 11, y, "Mobile")
    cbx2 = cbx + 11 + c.stringWidth("Mobile   ", "Serif", 9)
    checkbox(c, cbx2, y - 1, size=8)
    c.drawString(cbx2 + 11, y, "Landline")
    end_x = cbx2 + 11 + c.stringWidth("Landline", "Serif", 9) + 2
    underline(c, end_x, rx, y - 1.5)
    y -= 16

    y = field(c, "Address",         lx, rx, y)
    y = field(c, "City, State, Zip", lx, rx, y)

    y -= 4
    rule(c, lx, y, rx)
    y -= 12

    # I am a
    c.setFont("Serif-Bold", 10.5)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(lx, y, sc("I am a:"))
    y -= 13

    for opt in ["First-time visitor", "Occasional visitor", "Regular attendee",
                "Member", "Out-of-town visitor"]:
        y = cbline(c, opt, lx, y, fs=10, gap=13)

    y -= 4
    rule(c, lx, y, rx)
    y -= 10

    # Privacy notice
    c.setFont("Serif-Italic", 8)
    c.setFillColorRGB(0.33, 0.33, 0.33)
    c.drawString(lx, y, "Your information is used only to connect with you")
    y -= 9
    c.drawString(lx, y, "and will never be sold or shared with outside parties.")
    c.setFillColorRGB(0, 0, 0)

# ── BACK card ─────────────────────────────────────────────────────────────────

def draw_back(c, ox, oy):
    lx = ox + PAD
    rx = ox + CW - PAD
    y  = oy + CH - PAD

    # Mini header
    c.setFont("Serif-Bold", 10.5)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(lx, y, sc("St. Paul\u2019s by-the-Lake") + "  \u2014  " + sc("Connect Card"))
    y -= 6
    rule(c, lx, y, rx, width=0.7)
    y -= 13

    # I would like to
    c.setFont("Serif-Bold", 10.5)
    c.drawString(lx, y, sc("I would like to:"))
    y -= 13

    for opt in [
        "Be added to your email list",
        "Speak with a priest or clergy member",
        "Learn more about membership",
        "Learn about volunteer opportunities",
        "Update my contact information",
        "Receive info about Christian formation",
    ]:
        y = cbline(c, opt, lx, y, fs=10, gap=13)

    y -= 4
    rule(c, lx, y, rx)
    y -= 12

    # Prayer request
    c.setFont("Serif-Bold", 10.5)
    c.drawString(lx, y, sc("Prayer Request"))
    y -= 11
    c.setFont("Serif", 9)
    c.drawString(lx, y, "Please share any prayer needs below.")
    y -= 15

    for _ in range(4):
        c.setStrokeColorRGB(0.5, 0.5, 0.5)
        c.setLineWidth(0.4)
        c.line(lx, y, rx, y)
        y -= 15

    y -= 2
    checkbox(c, lx, y - 1, size=8)
    c.setFont("Serif", 9)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(lx + 12, y, "Share with prayer team")
    cbx2 = lx + 12 + c.stringWidth("Share with prayer team     ", "Serif", 9)
    checkbox(c, cbx2, y - 1, size=8)
    c.drawString(cbx2 + 12, y, "Keep private")
    y -= 13

    rule(c, lx, y, rx)
    y -= 12

    # How did you hear
    c.setFont("Serif-Bold", 10.5)
    c.drawString(lx, y, sc("How did you hear about us?"))
    y -= 13

    for opt in ["Friend or family", "Website or social media",
                "Walked or drove by", "Community event", "Other"]:
        y = cbline(c, opt, lx, y, fs=10, gap=13)

    y -= 4
    rule(c, lx, y, rx)
    y -= 10

    # Privacy notice
    c.setFont("Serif-Italic", 8)
    c.setFillColorRGB(0.33, 0.33, 0.33)
    c.drawString(lx, y, "Your information is used only to connect with you")
    y -= 9
    c.drawString(lx, y, "and will never be sold or shared with outside parties.")
    c.setFillColorRGB(0, 0, 0)

# ── Build PDF ─────────────────────────────────────────────────────────────────

def main():
    c = canvas.Canvas(OUTPUT, pagesize=letter)
    c.setTitle("St. Paul's by-the-Lake Connect Cards")

    for ox, oy in ORIGINS:
        draw_front(c, ox, oy)
    c.showPage()

    for ox, oy in ORIGINS:
        draw_back(c, ox, oy)
    c.showPage()

    c.save()
    print(f"Saved: {OUTPUT}")

if __name__ == "__main__":
    main()
