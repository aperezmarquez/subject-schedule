# Read all the subjects
import pytesseract as tsr
from PIL import Image

# Gets all the critical points of the img
def get_critical_points(width, height):
    # Remove subject times and days of the week
    left_img_error = width*0.04
    top_img_error = height*0.1
    # Get column width and row height
    column_width = (width - left_img_error) / 5
    row_height = (height - top_img_error) / 6

    return (left_img_error, top_img_error, column_width, row_height)

def check_subject(subject_row, subject_info):
    start_hour = 7 + subject_row*2
    end_hour = start_hour + 2

    lines = subject_info.splitlines()
    lines = [l for l in lines if l.strip()]
    if (len(lines) < 5):
        return

    i=0
    if (lines[1].replace(".", "").replace(":", "").replace("0", "").strip().isdigit()):
        print("change")
        i += 1

    print(lines[i])
    print(lines[i+1])
    print(lines[i+2])
    print(lines[i+3])
    print(lines[i+4])
    print("\n")

# Reads all the subjects of the calendar
def read_subjects(fileName):
    img = Image.open(fileName)
    width, height = img.size
    
    subject = {}

    # Sacamos los puntos criticos
    left_img_error, top_img_error, column_width, row_height = get_critical_points(width, height)

    for i in range(0, 6):
        crop_subject(img, left_img_error, top_img_error, column_width, row_height, i)
        

def crop_subject(img, left_img_error, top_img_error, column_width, row_height, day):
    # Calculate left and right x values where to crop
    x_start_point = left_img_error + (day*column_width)
    x_end_point = x_start_point + column_width

    # Get every class in the day
    for j in range(0, 6):
        # Calculate top and bottom y values
        y_start_point = top_img_error + (j * row_height)
        y_end_point = y_start_point + (j + 1 * row_height)

        # Asign coordinates and crop the img
        coordinates = (x_start_point, y_start_point, x_end_point, y_end_point)
        img_cropped = img.crop(coordinates)
    
        text = tsr.image_to_string(img_cropped, lang='spa')
        check_subject(j, text)

def convert_to_json(fileName, day):
    pass

if __name__ == '__main__':
    read_subjects('MAIS2_segundo_cuatri.png')
