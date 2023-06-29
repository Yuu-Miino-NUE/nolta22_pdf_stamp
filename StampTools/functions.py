import io
from typing import Literal, BinaryIO

from PyPDF2 import PdfWriter, PdfReader, PageObject
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import utils
from reportlab.lib.units import cm, mm

NumberEnclosure = Literal["en_dash", "em_dash", "minus", "parens", "page", "Page"]

NUMBER_ENCLOSURE_DICT = {
    "en_dash": ["\u2013 ", " \u2013"],
    "em_dash": ["\u2014 ", " \u2014"],
    "minus": ["- ", " -"],
    "parens": ["(", ")"],
    "page": ["p.", ""],
    "Page": ["P.", ""],
}


def _format_number(num: int, encl: NumberEnclosure) -> str:
    start, end = NUMBER_ENCLOSURE_DICT[encl]

    utf_string = f"{start}{str(num)}{end}"
    return "{}".format(utf_string)


# Font handling
FONT = "Times"
pdfmetrics.registerFont(TTFont("Times", "StampTools/ttfs/Times New Roman.ttf"))
pdfmetrics.registerFont(TTFont("Timesi", "StampTools/ttfs/Times New Roman Italic.ttf"))
pdfmetrics.registerFont(TTFont("Timesbd", "StampTools/ttfs/Times New Roman Bold.ttf"))
pdfmetrics.registerFontFamily(
    FONT,
    normal="Times",
    bold="Timesbd",
    italic="Timesi",
)


# Main functions
def _put_page_numbers(
    buffer: BinaryIO,
    base_pdf: PdfReader,
    start_page: int,
    num_height: float,
    encl: NumberEnclosure,
):
    _c = canvas.Canvas(buffer)  # Associate canvas with buffer
    for i in range(len(base_pdf.pages)):
        page_size = _get_page_size(base_pdf.pages[i])
        _c.setPageSize(page_size)  # Width and height of page
        _c.setFont(FONT, 11)
        _c.drawCentredString(
            page_size[0] / 2.0, num_height, _format_number(start_page + i, encl)
        )
        _c.showPage()  # Close current and start new page
    _c.save()


def _get_page_size(page: PageObject) -> tuple[float, float]:
    page_box = page.mediabox
    width = page_box.right - page_box.left
    height = page_box.top - page_box.bottom
    return float(width), float(height)


def stamp_pdf(
    input: str,
    output: str,
    first_page_overlay: str | None = None,
    encl: NumberEnclosure = "em_dash",
    start_num: int = 1,
    num_height: float = 10.5 * mm,
) -> int:
    """Make a stamped PDF from a template PDF.

    Parameters
    ----------
    input : str
        Filename of a base PDF.
    output : str
        Output filename of the stamped PDF.
    encl : NumberEnclosure, optional
        Enclosure of a page number, by default "em_dash"
    start_num : int, optional
        Page number of the first page, by default 1
    num_height : float, optional
        Height of the position of page numbers, by default 10.5*mm

    Returns
    -------
    int
        `start_num` + number of pages of the base PDF.
    """
    if first_page_overlay is not None:
        try:
            _fpo = PdfReader(open(first_page_overlay, "rb")).pages[0]
        except:
            raise FileExistsError("No header logo PDF found. Please create one first.")
    else:
        _fpo = None

    try:
        base_pdf = PdfReader(open(input, "rb"))
    except:
        raise FileExistsError("No PDF found at input.")

    with io.BytesIO() as buffer:
        # Create page overlaying pdf in buffer
        _put_page_numbers(buffer, base_pdf, start_num, num_height, encl)
        all_overlays = PdfReader(buffer).pages

        # Put logo on first page of overlay if exist
        if _fpo is not None:
            all_overlays[0].merge_page(_fpo)
            all_overlays[0].compress_content_streams()

        # Put numbers on the base page and add it to the output
        writer = PdfWriter()
        for _base, _overlay in zip(base_pdf.pages, all_overlays):
            _base.merge_page(_overlay)
            writer.add_page(_base)

        # Write to output file
        with open(output, "wb") as f:
            writer.write(f)

    return len(base_pdf.pages) + start_num


def _get_height(path: str, width: float = 1 * cm) -> float:
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return width * aspect


def _put_text(
    c: canvas.Canvas, line: str, pos_x: float, pos_y: float, fontsize: int = 8
) -> None:
    t = c.beginText()
    t.setFont(FONT, fontsize)
    t.setTextOrigin(pos_x, pos_y)
    t.textLine(line)
    c.drawText(t)


def put_logo_with_text(
    output: BinaryIO,
    text_lines: list[str] = [],
    logo_file: str | None = None,
    pos_x: float = 84 * mm,
    pos_y: float = 272 * mm,
    logo_width: float = 18 * mm,
    fontsize: int = 8,
):
    """Put logo and text on a PDF.

    Parameters
    ----------
    output : BinaryIO
        Output buffer.
    text_lines : list[str], optional
        Text lines to put, by default []
    logo_file : str | None, optional
        Logo file, by default None
    pos_x : float, optional
        Horizontal position, by default 84*mm
    pos_y : float, optional
        Vertical position, by default 272*mm
    logo_width : float, optional
        Width of logo, by default 18*mm
    fontsize : int, optional
        Font size, by default 8
    """

    # Create destination canvas
    pdf_canvas = canvas.Canvas(output, pagesize=A4)

    # Insert logo if not None
    if logo_file is not None:
        logo_height = _get_height(logo_file, logo_width)
        pdf_canvas.drawImage(
            logo_file, pos_x, pos_y, width=logo_width, height=logo_height, mask="auto"
        )
    else:
        logo_width = 0
        logo_height = 0

    # Insert text if not empty
    if len(text_lines) != 0:
        base_x = pos_x + (logo_width * 1.15)
        base_y = pos_y + (logo_height / 2.0 + (1.0 * mm * (len(text_lines) - 1)))

        for i, l in enumerate(text_lines):
            _put_text(pdf_canvas, l, base_x, base_y - (4 * mm * i), fontsize)

    # Save canvas
    pdf_canvas.save()
