from pylibdmtx.pylibdmtx import encode
from PIL import Image
encoded = encode('121341'.encode('ASCII'))
img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
img.save('dmtx.png')
