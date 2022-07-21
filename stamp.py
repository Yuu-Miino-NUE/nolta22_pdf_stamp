import io
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

# User Settings
FROM_CORNER_Y = 10.5*mm

def format_number(num: str):
    en_dash = "\u2013" # UTF-8 only
    em_dash = "\u2014" # UTF-8 only
    utf_string = f"{en_dash} {num} {en_dash}"
    return u"{}".format(utf_string)

# Font handling
FONT = "Times"
pdfmetrics.registerFont(TTFont('Times','./ttfs/Times New Roman.ttf'))
pdfmetrics.registerFont(TTFont('Timesi','./ttfs/Times New Roman Italic.ttf'))
pdfmetrics.registerFont(TTFont('Timesbd','./ttfs/Times New Roman Bold.ttf'))
pdfmetrics.registerFontFamily(FONT, normal='Times', bold='Timesbd', italic='Timesi',)

# Main functions
def create_page_number_pdf(c: canvas.Canvas, page_size: tuple, page_num: int):
    c.setPageSize(page_size)
    c.setFont(FONT, 11)
    c.drawCentredString(page_size[0] / 2.0, FROM_CORNER_Y, format_number(page_num))
    c.showPage()
    
def get_page_size(page) -> tuple:
    page_box = page.mediaBox
    width  = page_box.getUpperRight_x() - page_box.getLowerLeft_x()
    height = page_box.getUpperRight_y() - page_box.getLowerLeft_y()
    return float(width), float(height)

def merge_pdf(input_file_path, output_file_path, start_num: int = 1):
    # ヘッダーにロゴアイコンがあるPDF全体の読み込み
    # ロゴアイコンがあるページ読み込み
    header_logo_pdf = PdfFileReader(open("pdf_template/header_logo.pdf", "rb"))
    header_logo_page = header_logo_pdf.getPage(0)

    # 既存のファイル読み込み
    # 既存のファイルのページ数を取得する
    input_file = PdfFileReader(open(input_file_path, 'rb'), strict=False)
    page_count = input_file.getNumPages()

    # 新規の出力ファイル作成
    output_file = PdfFileWriter()

    # ページ番号のみのダミー PDF をバッファに保存
    bs = io.BytesIO()
    c = canvas.Canvas(bs)
    for i in range(0, page_count):
        pdf_page = input_file.getPage(i)
        page_size = get_page_size(pdf_page)
        create_page_number_pdf(c, page_size, i+start_num)
    c.save()

    pdf_num_reader = PdfFileReader(bs)

    # 既存の全体ページをループで回す
    for page_number in range(page_count):
        input_page = input_file.getPage(page_number)
        pdf_num    = pdf_num_reader.getPage(page_number)

        # ページ番号
        input_page.mergePage(pdf_num)

        # トップページ（ロゴ）
        if page_number == 0:
            # 既存のページとヘッダーロゴをmergeする
            input_page.mergePage(header_logo_page)
            # 圧縮する
            input_page.compressContentStreams()

        # 出力ファイルにページを追加する
        output_file.addPage(input_page)

    # 出力ファイル保存
    with open(output_file_path, "wb") as outputStream:
        output_file.write(outputStream)

    bs.close()

merge_pdf('./nolta2022.pdf', './out.pdf')
