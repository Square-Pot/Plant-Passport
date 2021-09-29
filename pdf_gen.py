import io
from pylibdmtx.pylibdmtx import encode
from PIL import Image
from fpdf import FPDF

def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format="PNG")
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

# data matrix generate
encoded = encode('121341'.encode('ASCII'))
dmtx_img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
dmtx_img_as_bytes = image_to_byte_array(dmtx_img)

print(type(dmtx_img_as_bytes))

#img.save('dmtx.png')

# pdf generate
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', '', 14)
pdf.ln(10)
pdf.write(5, 'hello world!')
pdf.image(dmtx_img_as_bytes, 50, 50,)
pdf.output('pdf-dmtx-test.pdf', 'F')