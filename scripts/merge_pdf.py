from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs(front_pdf, back_pdf, output_pdf):
    # Open both PDF files
    reader_front = PdfReader(front_pdf)
    reader_back = PdfReader(back_pdf)
    writer = PdfWriter()

    # Reverse the order of pages in back_pdf
    back_pages = list(reversed(reader_back.pages))

    # Assuming both PDFs have the same number of pages
    for i in range(len(reader_front.pages)):
        writer.add_page(reader_front.pages[i]) # Add front page
        writer.add_page(back_pages[i])         # Add back page in reversed order

    # Write to the output PDF
    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)

# Usage
merge_pdfs('A.pdf', 'B.pdf', 'Merged.pdf')