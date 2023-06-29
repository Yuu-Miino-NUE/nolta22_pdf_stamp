def test_stamp():
    from os.path import exists
    from StampTools import stamp_pdf, mm

    FPO_PATH = "pdf_template/first_page_overlay.pdf"

    # If not exists template PDF for Logo
    if not exists(FPO_PATH):
        from StampTools import put_logo_with_text

        logo_pos_x = 84 * mm
        logo_pos_y = 272 * mm
        logo_width = 18 * mm
        logo_file = "./img/logo.png"
        text_lines = [
            "2022 International Symposium on Nonlinear Theory and Its Applications,",
            "NOLTA2022, Virtual, December 12-15, 2022",
        ]

        with open(FPO_PATH, "wb") as f:
            put_logo_with_text(
                f, text_lines, logo_file, logo_pos_x, logo_pos_y, logo_width
            )

    # Stamp PDF (add logo and page numbers)
    item_list = [{"input": "./nolta2022.pdf", "output": "./nolta2022_stamped.pdf"}]

    print(f"Count of PDFs to proceed: {len(item_list)}")
    start_num = 1
    for item in item_list:
        print(f"proceeding stamp: {item['input']} -> {item['output']} ... ", end="")
        start_num = stamp_pdf(
            item["input"],
            item["output"],
            first_page_overlay=FPO_PATH,
            encl="em_dash",
            start_num=start_num,
        )
        print("done")
