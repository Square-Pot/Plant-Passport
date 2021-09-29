from fpdf import FPDF
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', '', 14)
pdf.ln(10)
pdf.write(5, 'hello world!')
pdf.image("dmtx.png", 50, 50)
pdf.output('pdf-test.pdf', 'F')