# StampTools for logo and page number

* Can add logos and page numbers on PDF without stripping any hyper-links

## Main Scheme
1. Make template PDF including logo in `pdf_template` directory (should do only once)
2. Make template PDF including page numbers in buffer (runs for every page implicitly)
3. Merge manuscript PDF and template PDFs (1 and 2)

In practice, only the function `create_header_logo_PDF` realizes the step 1;
another function `stamp_pdf` realizes step 2 and 3.
The script file `add_stamp.py` shows an example usage including all of them.

## Usage of functions
### `stamp_pdf`
#### Parameters
* `input_file_path`
* `output_file_path`
* `encl`: enclosure of the page number  
  (available options: `"en_dash", "em_dash", "minus", "parens", "page", "Page"`)
* `start_num`: page number of the first page for the input file
* `num_height`: height of the page number

#### Return
* start_num for next loop

### `create_header_logo_PDF`
#### Parameters
* `logo_file_path`
* `pos_x`: horizontal position of logo
* `pos_y`: vertical position of logo
* `logo_width`: width of logo (height will automatically change with keeping aspect ratio)
* `lines`: list of sentences to show on the right side of the logo

#### Return
None

## References
* https://serip39.hatenablog.com/entry/2021/01/18/170000
* https://gammasoft.jp/python-example/python-add-page-number-to-pdf/
