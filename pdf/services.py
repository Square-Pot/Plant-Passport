
import io
from django.templatetags.static import static
from pylibdmtx.pylibdmtx import encode
import PIL
from PIL import Image
from fpdf import FPDF

# Data Matrix size
IMG_WIDTH = 40  # px

# Resolution calulation according to observation: 50px = 18mm
PX_in_MM = 2.7


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
    dmtx_img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)  # Image size is 70x70 px, where margins are 10px
    dmtx_img = dmtx_img.crop((10, 10 , 60, 60))                                         # Crop white margins. Resulting image size is: 50x50 px
    dmtx_img = dmtx_img.resize((IMG_WIDTH, IMG_WIDTH), resample=PIL.Image.LANCZOS)      # Resize to IMG_WIDTH square. Think what TODO when this matrix-size will exhaust
    return dmtx_img

def generate_labels_pdf(rich_plants:list):
    pdf = _create_pdf()

    # start point
    x, y = 10, 10

    for rp in rich_plants:
        puid = rp.uid

        # preparing data 
        dm_img = _generate_datamatrix(puid)

        if rp.attrs.number:
            field_num = rp.attrs.number.upper()
        else:
            field_num = None

        if rp.attrs.genus:
            #genus = rp.attrs.genus.capitalize()
            genus = rp.attrs.genus.capitalize()[0] + '.'
        else:
            field_num = None

        if rp.attrs.species:
            species = rp.attrs.species.lower()
        else:
            species = None
        
        if rp.attrs.subspecies:
            subspecies = rp.attrs.subspecies.lower()
        else:
            subspecies = None

        if rp.attrs.variety:
            variety = rp.attrs.variety.lower()
        else:
            variety = None

        if rp.attrs.cultivar:
            cultivar = rp.attrs.cultivar.title()
        else:
            cultivar = None

        if rp.attrs.affinity:
            affinity = rp.attrs.affinity.title()
        else:
            affinity = None

        if rp.attrs.ex:
            ex = rp.attrs.ex.title()
        else:
            ex = None

        # Image
        pdf.set_xy(x, y)
        pdf.image(dm_img, x=x, y=y)

        # Field number
        fn_shift_x = IMG_WIDTH // PX_in_MM
        fn_shift_y = IMG_WIDTH // PX_in_MM
        x += fn_shift_x
        y += fn_shift_y

        pdf.set_xy(x, y)
        pdf.set_font_size(10)
        cell_width_fn = IMG_WIDTH // PX_in_MM
        cell_high_fn = 6
        text = ''
        if field_num:
            text = field_num
        with pdf.rotation(90):
            pdf.cell(cell_width_fn, cell_high_fn, text, border=1, align="C")

        # Gen. + sp. + ssp.
        x += cell_high_fn
        y -= cell_width_fn

        pdf.set_xy(x, y)
        cell_width = 60
        cell_high = IMG_WIDTH // PX_in_MM / 3
        pdf.set_font_size(10)
        text = ''
        if genus: 
            text += genus
        if species:
            text += f' {species}'
        if subspecies:
            text += f' ssp. {subspecies}'
        pdf.cell(cell_width, cell_high, text, border=1)

        # var. + cv.
        y +=  cell_high
        pdf.set_xy(x, y)
        text = '  '
        if variety:
            text += f'v. {variety}'
        if cultivar:
            text += f' cv. {cultivar}'
        pdf.cell(cell_width, cell_high, text, border=1)

        # aff. + ex. 
        y +=  cell_high
        pdf.set_xy(x, y)
        text = '  '
        if affinity:
            text += f'aff. {affinity}'
        if ex:
            text += f' ex. {ex}'
        pdf.cell(cell_width, cell_high, text, border=1)
        
        #
        bb = x
        #x = bb - fn_shift_x - cell_high_fn - cell_width
        x = 10
        y += 8


    filename = 'pdf-dmtx-test.pdf'
    pdf.output('pdf-dmtx-test.pdf', 'F')

    return filename

        

        





    return "path_to_file"