
import io
from django.templatetags.static import static
from pylibdmtx.pylibdmtx import encode
import PIL
from PIL import Image
from fpdf import FPDF

# Data Matrix size
DMTX_IMG_WIDTH = 40  # px

# Resolution calulation according to observation: 50px = 18mm
PX_in_MM = 2.7

# A4 Page high
PAGE_HIGH = 297

# Vertical Space between labels
V_SPACE = 8

# Vertical Number of Labels
V_NUM = PAGE_HIGH // (( DMTX_IMG_WIDTH // PX_in_MM ) + V_SPACE )

# Show Borders
SHOW_BRD = 0

# Start coordinates on page
START_X = 10
START_Y = 10


class Labels:

    def __init__(self, rich_plants:list):
        self.rich_plants = rich_plants
        self.dmtx_side_px = 40      # size of data matrix image in pixels
        self.ppmm = 2.7             # pixels per mm
        self.page_high = 297        # high of A4 
        self.v_space = 8            # vertical space between labels
        self.start_x = 10           # x of origin
        self.start_y = 10           # y of origin 
        self.show_brd = 0           # showing of borders in cells
        self.dmtx_side_mm = self.dmtx_side_px /  self.ppmm  # size of data matrix image in mm

        self.pdf = self._create_pdf()


    def _create_pdf(self)->FPDF:
        """PDF-object create and setup"""
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu_regular', fname='static/DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu_regular', size=10)
        return pdf

    def _generate_datamatrix(self, text)->Image:
        """Data matrix generate"""
        encoded = encode(text.encode('ASCII'))
        dmtx_img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)              # Image size is 70x70 px, where margins are 10px
        dmtx_img = dmtx_img.crop((10, 10 , 60, 60))                                                     # Crop white margins. Resulting image size is: 50x50 px
        dmtx_img = dmtx_img.resize((DMTX_IMG_WIDTH, DMTX_IMG_WIDTH), resample=PIL.Image.LANCZOS)        # Resize to IMG_WIDTH square. Think what TODO when this matrix-size will exhaust
        return dmtx_img

    def generate_labels_pdf(self):
        

        # start point
        x = START_X
        y = START_Y

        label_count = 0
        column_num = 1


        for rp in rich_plants:
            label_count += 1 
            if label_count > V_NUM and column_num == 1:
                x = START_X + 100
                y = START_Y
                label_count = 1
                column_num = 2
            elif label_count > V_NUM and column_num == 2:
                x = START_X
                label_count = 1
                column_num = 1 
                pdf.add_page()

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

            
            fn_shift_x = DMTX_IMG_WIDTH // PX_in_MM
            fn_shift_y = DMTX_IMG_WIDTH // PX_in_MM
            x += fn_shift_x

            # Frame 
            pdf.set_xy(x + 1, y)
            pdf.cell(70, DMTX_IMG_WIDTH // PX_in_MM, '', border=1)

            # Field number
            y += fn_shift_y
            pdf.set_xy(x, y)
            pdf.set_font_size(10)
            cell_width_fn = DMTX_IMG_WIDTH // PX_in_MM
            cell_high_fn = 6
            text = ''
            if field_num:
                text = field_num
            with pdf.rotation(90):
                pdf.cell(cell_width_fn, cell_high_fn, text, border=SHOW_BRD, align="C")
                



            

            # Gen. + sp. + ssp.
            x += cell_high_fn
            y -= cell_width_fn

            pdf.set_xy(x, y)
            cell_width = 60
            cell_high = DMTX_IMG_WIDTH // PX_in_MM / 3
            pdf.set_font_size(10)
            text = ''
            if genus: 
                text += genus
            if species:
                text += f' {species}'
            if subspecies:
                text += f' ssp. {subspecies}'
            pdf.cell(cell_width, cell_high, text, border=SHOW_BRD)

            # var. + cv.
            y +=  cell_high
            pdf.set_xy(x, y)
            text = '  '
            if variety:
                text += f'v. {variety}'
            if cultivar:
                text += f' cv. {cultivar}'
            pdf.cell(cell_width, cell_high, text, border=SHOW_BRD)

            # aff. + ex. 
            y +=  cell_high
            pdf.set_xy(x, y)
            text = '  '
            if affinity:
                text += f'aff. {affinity}'
            if ex:
                text += f' ex. {ex}'
            pdf.cell(cell_width, cell_high, text, border=SHOW_BRD)
            
            #
            bb = x
            #x = bb - fn_shift_x - cell_high_fn - cell_width
            x = 10
            y += V_SPACE


        filename = 'pdf-dmtx-test.pdf'
        pdf.output('pdf-dmtx-test.pdf', 'F')

        return filename

        

        





    return "path_to_file"