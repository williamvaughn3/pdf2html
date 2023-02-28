#!/usr/bin/env python3

import os
import PyPDF2
import pytesseract
from PIL import Image
import fitz
import argparse

def check_dependas():
    try:
        import PyPDF2
        import pytesseract
        import fitz
        import argparse
    except ImportError as e:
        print(f'Error: {e}')
        print('Please install the missing dependencies, you can do so by running the following command:')
        print('pip install -r requirements.txt')
        exit(1)

def convert_pdf_to_html_with_ocr(input_file, output_file, image_dir):
    pdf_reader = PyPDF2.PdfFileReader(open(input_file, 'rb'))
    html_data = ''

    for page_num in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page_num)
        html_data += f'<h1>Page {page_num+1}</h1>\n'
        pages_text = page.extractText()
        html_data += f'<pre>{pages_text}</pre>\n'
        images = page.get('/XObject')
        if images:
            for obj in images:
                os.system(f'cp {obj} {os.path.join(os.path.dirname(image_dir), os.path.basename(obj) )}')
                stream = obj.getObject()
                if stream.get('/Subtype') == '/Image':
                    width = stream['/Width']
                    height = stream['/Height']
                    color_space = stream['/ColorSpace']
                    if color_space == '/DeviceRGB':
                        mode = 'RGB'
                    else:
                        mode = 'P'
                    bits = stream['/BitsPerComponent']
                    image_name = os.path.join(image_dir, f'image{page_num}_{obj.num}.png')
                    pixmap = fitz.Pixmap(fitz.csRGB, stream)
                    img = Image.frombytes(mode, [pixmap.width, pixmap.height], pixmap.samples)
                    img.save(image_name)
                    image_path = os.path.relpath(image_name, os.path.dirname(output_file))
                    html_data += f'<pre>{pytesseract.image_to_string(Image.open(image_name))}</pre>\n'
                    html_data += f'<img src="{image_path}" width="{width}" height="{height}" alt="page{page_num}_image{obj.num}" />\n'
                    html_data += f'<pre>{pytesseract.image_to_string(img)}</pre>\n'

    with open(output_file, 'w') as f:
        f.write(html_data)  

def checkArgs():
    parser = argparse.ArgumentParser(description='Process PDF and HTML files.')
    parser.add_argument('input_file', metavar='<Input_File.pdf>', type=str,
                        help='Existing PDF File to Process')
    parser.add_argument('output_file', metavar='<File_to_Output.html>', type=str,
                        help='HTML File that Will be Created')
    parser.add_argument('image_dir', metavar='PATH/TO/IMAGE/DIR', type=str,
                        optional=True, default='images', help='Choose an existing directory')
    args = parser.parse_args()
    if not os.path.isfile(args.input_file) or not args.input_file.endswith('.pdf'):
        parser.error('PDF file doesn\'t exist, or does not have .pdf extension')
    if os.path.isfile(args.output_file):
        parser.error('.html extension must be used, or file already exists.')
    if not os.path.isdir(args.image_dir):
        os.mkdir('images')
        args.image_dir = 'images'
    return args


def main():
    check_dependas
    args = checkArgs()
    convert_pdf_to_html_with_ocr(args.input_file, args.output_file, args.image_dir)
	
if __name__ == "__main__":
    main()
    