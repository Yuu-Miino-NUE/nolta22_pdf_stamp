from io import BytesIO
from StampTools import stamp_pdf, mm, PdfReader, put_logo_with_text, put_image, put_text

kwargs = {
    "text_lines": [
        "2022 International Symposium on Nonlinear Theory and Its Applications,",
        "NOLTA2022, Virtual, December 12-15, 2022",
    ],
    "logo_file": "./img/logo.png",
    "pos_x": 84 * mm,
    "pos_y": 272 * mm,
    "logo_width": 18 * mm,
    "fontsize": 8,
}


def test_put_logo_with_text_to_buffer():
    put_logo_with_text(output=BytesIO(), **kwargs)


def test_put_logo_with_text_to_file():
    with open("pdf_template/first_page_overlay.pdf", "wb") as f:
        put_logo_with_text(output=f, **kwargs)


def test_put_image():
    put_image(
        "pdf_template/first_page_overlay.pdf",
        "./img/by-nc-nd.png",
        21.3 * mm,
        20 * mm,
        19.5 * mm,
    )


def test_put_text():
    put_text(
        "pdf_template/first_page_overlay.pdf",
        [
            "This work is licensed under a Creative Commons",
            "Attribution NonCommercial, No Derivatives 4.0 License.",
        ],
        43.3 * mm,
        24.2 * mm,
        7,
    )


def test_stamp():
    try:
        f = open("pdf_template/first_page_overlay.pdf", "rb")
    except FileNotFoundError:  # If not exists template PDF for Logo
        f = BytesIO()
        put_logo_with_text(output=f, **kwargs)

    # Stamp PDF (add logo and page numbers)
    item_list = [{"input": "./nolta2022.pdf", "output": "./nolta2022_stamped.pdf"}]

    print(f"Count of PDFs to proceed: {len(item_list)}")
    start_num = 1
    for item in item_list:
        print(f"proceeding stamp: {item['input']} -> {item['output']} ... ", end="")
        start_num = stamp_pdf(
            item["input"],
            item["output"],
            first_page_overlay=PdfReader(f),
            encl="en_dash",
            start_num=start_num,
        )
        print("done")
