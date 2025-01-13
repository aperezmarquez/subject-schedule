# Read all the subjects
import pytesseract as tsr
from PIL import Image

def read_subjects(fileName, day):
    img = Image.open(fileName)
    width, height = img.size
    
    crop_subject(img, width, height, day)

def crop_subject(img, width, height, day):
    # Remove subject times and days of the week
    left_img_error = width*0.04
    top_img_error = height*0.1
    # Get the column width
    column_width = (width - left_img_error) / 5

    # Calculate the top left corner where we want to crop
    x_start_point = left_img_error + (day*column_width)
    y_start_point = top_img_error

    # Calculate the bottom right corner
    x_end_point = x_start_point + column_width
    y_end_point = y_start_point + height

    coordenadas = (x_start_point, y_start_point, x_end_point, y_end_point)
    img_cropped = img.crop(coordenadas)
    
    text = tsr.image_to_string(img_cropped, lang='spa')
    print(text)

def convert_to_json(fileName, day):
    pass

if __name__ == '__main__':
    read_subjects('MAIS2_segundo_cuatri.png', 1)
