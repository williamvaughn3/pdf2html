# Python PDF to HTML w/ ocr



## Description

Usecase was for a data aggregation test as a way to get data to pandoc and 
into ELK.

Goals:

- [ ] Parse PDF and use OCR on images to add create flat html file.
- [ ] That can be easily parsed by pandoc.

Not fully tested, but it worked for my use case.
Use at your own risk.

## Requirements
pytesseract
PyMuPDF
argparse

## Usage

```
#git clone this repo
#cd /dir
pip install -r requirements.txt
chmod +x PDFHTML.py
./PDFHTML.py input.pdf output.html path/image/output/dir
python3 script input.pdf output.html path/image/output/dir

```
## license

This project is licensed under the terms of the MIT license.

