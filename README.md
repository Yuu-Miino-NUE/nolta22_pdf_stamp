# StampTools for logo and page number stamping on PDF
## Main Scheme
1. Make template PDF including logo (should be only once)
2. Make buffer PDF including page numbers (runs for every page implicitly)
3. Merge manuscript PDF and template PDFs (1 and 2)

In practice, only the function `create_header_logo_PDF` realizes the step 1;
another function `stamp_pdf` realizes step 2 and 3.
The script file `add_stamp.py` includes all of them.

## Requirements
* PyPDF2 v2.6.0 ([pypi package](https://pypi.org/project/PyPDF2/2.6.0/))
* ReportLab v3.6.11 ([pypi package](https://pypi.org/project/reportlab/3.6.11/))

