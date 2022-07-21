# StampTools for logo and page number stamping on PDF
## Main Scheme
1. Make template PDF including logo in `pdf_template` directory (should do only once)
2. Make template PDF including page numbers in buffer (runs for every page implicitly)
3. Merge manuscript PDF and template PDFs (1 and 2)

In practice, only the function `create_header_logo_PDF` realizes the step 1;
another function `stamp_pdf` realizes step 2 and 3.
The script file `add_stamp.py` shows an example usage including all of them.

## Requirements
* PyPDF2 v2.6.0 ([pypi package](https://pypi.org/project/PyPDF2/2.6.0/))
* ReportLab v3.6.11 ([pypi package](https://pypi.org/project/reportlab/3.6.11/))

## Usage
### `stamp_pdf`
Parameters for the function `stamp_pdf` are as follows:
* input_file_path
* output_file_path
* encl: enclosure of the page number 
  (available optiosn: "en_dash", "em_dash", "minus", "parens", "page", "Page")
* start_num: page number of the first page of the input file
* num_height: height of the page number

## References
* https://serip39.hatenablog.com/entry/2021/01/18/170000
* https://gammasoft.jp/python-example/python-add-page-number-to-pdf/
