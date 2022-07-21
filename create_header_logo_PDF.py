from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import utils
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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
    

def create_header_logo_PDF():
    # 新規PDF作成
    pdf_canvas = canvas.Canvas('pdf_template/header_logo.pdf', pagesize=A4)

    # 画像を挿入する
    target_x, target_y = 84*mm, 272*mm
    logo_name = './img/logo.png'
    logo_width = 18*mm
    logo_height = get_height(logo_name, logo_width)
    pdf_canvas.drawImage(logo_name, target_x, target_y,
                         width=logo_width, height=logo_height, mask='auto')

    base_x = target_x+logo_width+3*mm
    base_y = target_y+logo_height-3.5*mm
    put_text(pdf_canvas, '2022 International Symposium on Nonlinear Theory and Its Applications,',
             base_x, base_y)
    put_text(pdf_canvas, 'NOLTA2022, Virtual, December 12-15, 2022',
             base_x, base_y-4*mm)

    # PDF保存
    pdf_canvas.save()


create_header_logo_PDF()
