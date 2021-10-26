from PIL import Image

photo = 'IMG_20211021_2212254.jpg'

def get_date_taken(path):
    return Image.open(path)._getexif()[36867]



date = get_date_taken(photo)

print(date)
