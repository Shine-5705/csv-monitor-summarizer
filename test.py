import pdfkit

path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

pdfkit.from_string("<h1>Hello PDF</h1>", "test.pdf", configuration=config)
print("PDF generated successfully.")
