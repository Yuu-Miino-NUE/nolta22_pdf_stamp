import io
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import utils
from reportlab.lib.units import cm, mm

HEADER_LOGO_PATH = "pdf_template/header_logo.pdf"

number_enclosure = {
    "en_dash": ["\u2013 ", " \u2013"],
    "em_dash": ["\u2014 ", " \u2014"],
    "minus": ["- ", " -"],
    "parens": ["(", ")"],
    "page": ["p.", ""],
    "Page": ["P.", ""]
}

def format_number(num: str, encl: str):
    start, end = number_enclosure[encl]

    utf_string = f"{start}{num}{end}"
    return u"{}".format(utf_string)

# Font handling
FONT = "Times"
pdfmetrics.registerFont(TTFont('Times','StampTools/ttfs/Times New Roman.ttf'))
pdfmetrics.registerFont(TTFont('Timesi','StampTools/ttfs/Times New Roman Italic.ttf'))
pdfmetrics.registerFont(TTFont('Timesbd','StampTools/ttfs/Times New Roman Bold.ttf'))
pdfmetrics.registerFontFamily(FONT, normal='Times', bold='Timesbd', italic='Timesi',)

# Main functions
def create_page_number_pdf(c: canvas.Canvas, page_size: tuple, page_num: int, num_height, encl):
    c.setPageSize(page_size)
    c.setFont(FONT, 11)
    c.drawCentredString(page_size[0] / 2.0, num_height, format_number(page_num, encl))
    c.showPage()
    
def get_page_size(page) -> tuple:
    page_box = page.mediaBox
    width  = page_box.getUpperRight_x() - page_box.getLowerLeft_x()
    height = page_box.getUpperRight_y() - page_box.getLowerLeft_y()
    return float(width), float(height)

def stamp_pdf(input_file_path, output_file_path, encl: str="em", start_num: int = 1, num_height = 10.5*mm):
    header_logo_pdf = PdfFileReader(open(HEADER_LOGO_PATH, "rb"))
    header_logo_page = header_logo_pdf.getPage(0)

    input_file = PdfFileReader(open(input_file_path, 'rb'), strict=False)
    page_count = input_file.getNumPages()

    output_file = PdfFileWriter()

    bs = io.BytesIO()
    c = canvas.Canvas(bs)
    for i in range(page_count):
        pdf_page = input_file.getPage(i)
        page_size = get_page_size(pdf_page)
        create_page_number_pdf(c, page_size, i+start_num, num_height, encl)
        
    c.save()

    pdf_num_reader = PdfFileReader(bs)

    for page_number in range(page_count):
        input_page = input_file.getPage(page_number)
        pdf_num    = pdf_num_reader.getPage(page_number)

        input_page.mergePage(pdf_num)

        if page_number == 0:
            input_page.mergePage(header_logo_page)
            input_page.compressContentStreams()

        output_file.addPage(input_page)

    with open(output_file_path, "wb") as outputStream:
        output_file.write(outputStream)

    bs.close()
    return page_count+start_num

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

def create_header_logo_PDF(logo_file_path: str, pos_x, pos_y, logo_width, lines):
    # Create destination canvas
    pdf_canvas = canvas.Canvas(HEADER_LOGO_PATH, pagesize=A4)
    logo_height = get_height(logo_file_path, logo_width)

    # Insert logo
    pdf_canvas.drawImage(logo_file_path, pos_x, pos_y,
                         width=logo_width, height=logo_height, mask='auto')

    base_x = pos_x+(logo_width*1.15)
    base_y = pos_y+(logo_height/2.0+(1.0*mm*(len(lines)-1)))

    for i, l in enumerate(lines):
        put_text(pdf_canvas, l, base_x, base_y-(4*mm*i))

    # Save canvas as a PDF
    pdf_canvas.save()

    
