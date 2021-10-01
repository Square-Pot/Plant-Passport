
import io
from django.templatetags.static import static
from pylibdmtx.pylibdmtx import encode
from PIL import Image
from fpdf import FPDF


def _create_pdf()->FPDF:
    """PDF-object create and setup"""
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu_regular', fname='static/DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu_regular', size=10)
    return pdf

def _generate_datamatrix(text)->Image:
    """Data matrix generate"""
    encoded = encode(text.encode('ASCII'))
    dmtx_img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    return dmtx_img


def generate_labels_pdf(rich_plants:list):
    pdf = _create_pdf()

    x, y = 60, 60

    for rp in rich_plants:
        puid = rp.uid

        dm_img = _generate_datamatrix(puid)
        field_num = rp.attrs.number.upper()

        genus = rp.attrs.genus.capitalize()
        species = rp.attrs.species.lower()
        subspecies = rp.attrs.subspecies.lower()
        variety = rp.attrs.variety.lower()
        cultivar = rp.attrs.cultivar.title()
        affinity = rp.attrs.affinity.title()
        ex = rp.attrs.ex.title()


        pdf.image(dm_img)

        with pdf.rotation(90, x=x, y=y):
            pdf.cell(20, 10, field_num)

        pdf.cell(40, 10, f'{genus} sp. {subspecies}')
        pdf.ln()
        pdf.cell(40, 10, f'{variety} sp. {cultivar}')


    filename = 'pdf-dmtx-test.pdf'
    pdf.output('pdf-dmtx-test.pdf', 'F')

    return filename

        

        





    return "path_to_file"