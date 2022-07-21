from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import utils
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# User settings
logo_pos_x = 84*mm
logo_pos_y = 272*mm
logo_width = 18*mm
logo_file = './img/logo.png'
lines = [
    '2022 International Symposium on Nonlinear Theory and Its Applications,',
    'NOLTA2022, Virtual, December 12-15, 2022'
]

# Font handling
FONT = "Times"
pdfmetrics.registerFont(TTFont('Times','./ttfs/Times New Roman.ttf'))
pdfmetrics.registerFont(TTFont('Timesi','./ttfs/Times New Roman Italic.ttf'))
pdfmetrics.registerFont(TTFont('Timesbd','./ttfs/Times New Roman Bold.ttf'))
pdfmetrics.registerFontFamily(FONT, normal='Times', bold='Timesbd', italic='Timesi',)

# Main functions
def get_height(path, width=1*cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return (width * aspect)

def put_text(c, line: str, pos_x, pos_y):
    t = c.beginText()
    t.setFont(FONT, 8)
    t.setTextOrigin(pos_x, pos_y)
    t.textLine(line)
    c.drawText(t)

def create_header_logo_PDF(logo_name: str, pos_x, pos_y, logo_width, lines):
    # Create destination canvas
    pdf_canvas = canvas.Canvas('pdf_template/header_logo.pdf', pagesize=A4)
    logo_height = get_height(logo_name, logo_width)

    # Insert logo
    pdf_canvas.drawImage(logo_name, pos_x, pos_y,
                         width=logo_width, height=logo_height, mask='auto')

    base_x = pos_x+(logo_width*1.15)
    base_y = pos_y+(logo_height/2.0+(1.0*mm*(len(lines)-1)))

    for i, l in enumerate(lines):
        put_text(pdf_canvas, l, base_x, base_y-(4*mm*i))

    # Save canvas as a PDF
    pdf_canvas.save()

# Run as a script
if __name__=="__main__":
    create_header_logo_PDF(logo_file, logo_pos_x, logo_pos_y, logo_width, lines)
