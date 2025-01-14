# Read all the subjects
import pytesseract as tsr
from PIL import Image
import json

# Gets all the critical points of the img
def get_critical_points(width, height):
    # Remove subject times and days of the week
    left_img_error = width*0.04
    top_img_error = height*0.1
    # Get column width and row height
    column_width = (width - left_img_error) / 5
    row_height = (height - top_img_error) / 6

    return (left_img_error, top_img_error, column_width, row_height)

# Checks and cleans the subject
def check_subject(subject_row, subject_info):
    start_hour = 9 + subject_row*2
    end_hour = start_hour + 2

    # Split the text from the image into lines and remove all spaces and empty lines
    lines = subject_info.splitlines()
    lines = [l for l in lines if l.strip()]
    # If the length is smaller than 1, then there is no subject
    if (len(lines) < 1):
        return -1
    elif (len(lines) < 4):
        return -2

    # We don't need the times of the class, so we remove them
    if (lines[0].replace(".", "").replace(":", "").strip().isdigit()):
        del lines[0]

    if (lines[-1].replace(".", "").replace(":", "").strip().isdigit()):
        del lines[-1]

    result = convert_to_json(lines, start_hour, end_hour)

    return result
        
# Crops the img into subjects
def crop_subject(img, left_img_error, top_img_error, column_width, row_height, day):
    # Calculate left and right x values where to crop
    x_start_point = left_img_error + (day*column_width)
    x_end_point = x_start_point + column_width

    day_subjects = []

    # Get every class in the day
    for j in range(0, 6):
        
        # Calculate top and bottom y values
        y_start_point = top_img_error + (j * row_height)
        y_end_point = y_start_point + (j + 1 * row_height)

        # Asign coordinates and crop the img
        coordinates = (x_start_point, y_start_point, x_end_point, y_end_point)
        img_cropped = img.crop(coordinates)

        # Saves all cropped images
        #img_cropped.save('images/subject_' + str(day) + '_' + str(j) + '.png')

        text = tsr.image_to_string(img_cropped, lang='spa')
        clean_subject = check_subject(j, text)

        if (clean_subject != -1 and clean_subject != -2):
            day_subjects.append(clean_subject)

    return day_subjects


# Reads all the subjects of the calendar
def read_subjects(fileName):
    img = Image.open(fileName)
    width, height = img.size

    week_subjects = {}

    # Sacamos los puntos criticos
    left_img_error, top_img_error, column_width, row_height = get_critical_points(width, height)

    for i in range(0, 5):
        day_subjects = crop_subject(img, left_img_error, top_img_error, column_width, row_height, i)
        
        week_subjects[i+1] = day_subjects

    week_subjects = json.dumps(week_subjects, indent=4)

    return week_subjects


# Converts the text read from the img to json
def convert_to_json(lines, start_hour, end_hour):
    subject = {
        "start_hour": start_hour,
        "course": lines[0],
        "subject": lines[1],
        "teacher": lines[2],
        "end_hour": end_hour,
    }

    return subject
