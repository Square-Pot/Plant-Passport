from PIL import Image
import datetime

photo = 'IMG_20211021_2212254.jpg'

def get_date_taken(path):
    return Image.open(path)._getexif()[36867]


dt_str = get_date_taken(photo)
dt = datetime.datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')
dt_ret = dt.strftime('%Y-%m-%d')




print(dt)
print(type(dt))
print(dt_ret)
