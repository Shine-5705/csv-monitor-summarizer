import pdfkit

html_string = "<h1>Hello PDF</h1>"
pdfkit.from_string(html_string, 'out.pdf')
