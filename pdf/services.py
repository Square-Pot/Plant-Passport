
import io
from pylibdmtx.pylibdmtx import encode
from PIL import Image
from fpdf import FPDF


def _create_pdf()->FPDF:
    """PDF-object create and setup"""
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu_regular', fname='DejaVuSansCondensed.ttf', uni=True)
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
        field_num = rp.ExtraAttrs.number.upper()

        genus = rp.ExtraAttrs.genus.capitalize()
        species = rp.ExtraAttrs.species.lower()
        subspecies = rp.ExtraAttrs.subspecies.lower()
        variety = rp.ExtraAttrs.variety.lower()
        cultivar = rp.ExtraAttrs.cultivar.title()
        affinity = rp.ExtraAttrs.affinity.title()
        ex = rp.ExtraAttrs.ex.title()


        pdf.image(dm_img)

        with pdf.rotation(90, x=x, y=y):
            pdf.cell(20, 10, field_num, x=x, y=y)

        pdf.cell(40, 10, f'{genus} sp. {subspecies}')
        pdf.ln()
        pdf.cell(40, 10, f'{variety} sp. {cultivar}')


    filename = 'pdf-dmtx-test.pdf'
    pdf.output('pdf-dmtx-test.pdf', 'F')

    return filename

        

        





    return "path_to_file"