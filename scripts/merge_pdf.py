import PyPDF2

def merge_pdfs(front_pdf, back_pdf, output_pdf):
    # Open both PDF files
    with open(front_pdf, 'rb') as file_front, open(back_pdf, 'rb') as file_back:
        reader_front = PyPDF2.PdfFileReader(file_front)
        reader_back = PyPDF2.PdfFileReader(file_back)
        writer = PyPDF2.PdfFileWriter()

        # Assuming both PDFs have the same number of pages
        for i in range(reader_front.getNumPages()):
            writer.addPage(reader_front.getPage(i)) # Add front page
            writer.addPage(reader_back.getPage(i))  # Add back page

        # Write to the output PDF
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

# Usage
merge_pdfs('A.pdf', 'B.pdf', 'Merged.pdf')
