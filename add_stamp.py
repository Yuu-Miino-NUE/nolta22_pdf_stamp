from reportlab.lib.units import cm, mm
from os.path import exists

from StampTools import stamp_pdf, HEADER_LOGO_PATH

# If not exists template PDF for Logo
if not exists(HEADER_LOGO_PATH):
    from StampTools import create_header_logo_PDF

    logo_pos_x = 84*mm
    logo_pos_y = 272*mm
    logo_width = 18*mm
    logo_file = './img/logo.png'
    lines = [
        '2022 International Symposium on Nonlinear Theory and Its Applications,',
        'NOLTA2022, Virtual, December 12-15, 2022'
    ]

    create_header_logo_PDF(logo_file, logo_pos_x, logo_pos_y, logo_width, lines)


# Stamp PDF (add logo and page numbers)
stamp_pdf('./nolta2022.pdf', './nolta2022_stamped.pdf', encl = "en_dash")

