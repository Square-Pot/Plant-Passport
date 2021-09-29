import io
from pylibdmtx.pylibdmtx import encode
from PIL import Image
from fpdf import FPDF


# data matrix generate
encoded = encode('121341'.encode('ASCII'))
dmtx_img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)

# pdf generate
pdf = FPDF()
pdf.add_page()
pdf.add_font('DejaVu_regular', fname='DejaVuSansCondensed.ttf', uni=True)
pdf.add_font('DejaVu_italic', fname='DejaVuSansCondensed-Oblique.ttf', uni=True)


pdf.set_font('DejaVu_regular', size=10)
pdf.ln(10)

text = u"""
Hello World
Приветики
"""

for txt in text.split('\n'):
  pdf.write(8, txt)
  pdf.ln(8)

pdf.set_font('DejaVu_italic', size=10)
pdf.ln(10)

text = u"""
Hello World
Приветики
"""

for txt in text.split('\n'):
  pdf.write(8, txt)
  pdf.ln(8)

pdf.image(dmtx_img, 50, 50,)
pdf.output('pdf-dmtx-test.pdf', 'F')