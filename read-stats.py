# import picamera
# import picamera.array
import cv2
import pytesseract
import time


def find_template(image, templates):
    matches = []
    for temp in templates:
        match = cv2.matchTemplate(image, temp, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
        matches.append(max_val)
    return max(matches)


def read_pause_menu(image, score_template, pause_templates, threshold):
    if threshold > 1:
        return "Please provide a number between 0 and 1 for the threshold."
    canny = cv2.Canny(image, 50, 200)
    score_val = find_template(canny, score_template)
    if score_val > 0.5:
        pause_val = find_template(canny, pause_templates)
        if pause_val < 0.5:
            return 1


def capture_image(camera):
    rawCapture = picamera.array.PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    time.sleep(.5)
    result = read_pause_menu(image, score_box_temp, templates, 0.5)
    if result == 1:
        return True, image
    else:
        rawCapture.truncate(0)
        return False, image


def find_largest_area(contours):
    area_list = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        area_list.append(area)
    area_list_sort = sorted(area_list)
    x, y, w, h = cv2.boundingRect(area_list_sort[-1])
    return x, y, w, h


def read_name(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (4, 4))
    dilated = cv2.dilate(image, kernel, iterations=5)
    img, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = find_largest_area(contours)
    cropped = image[y:y + h, x:x + w]
    return cropped


def read_image(image, type):
    thresh = cv2.adaptiveThreshold(image,
                                   255,
                                   cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV,
                                   31,
                                   21)
    cv2.imshow('image', thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if type.lower() == "name":
        image_iso = read_name()
        text = pytesseract.image_to_string(image_iso,
                                           config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 7 -oem 2 no_dict")
        return text
    elif type.lower() == 'score':
        text = pytesseract.image_to_string(image_iso, config="-c tessedit_char_whitelist=1234567890 -psm 6")
        return text
    else:
        return "Please define the type of picture. It's either a 'name' or 'score'."


def crop_image(image):
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(imgray, 150, 255, cv2.THRESH_BINARY)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area_list = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        area_list.append(area)

    area_list_sorted = sorted(area_list)
    cnt_ind = area_list.index(area_list_sorted[-1])

    x, y, w, h = cv2.boundingRect(contours[cnt_ind])
    score_box = imgray[y:y + h, x:x + w]
    score_box = cv2.resize(score_box, (1000, 1000))
    home_score = score_box[40:220, 400:475]
    home_team = score_box[40:165, 150:250]
    away_score = score_box[40:220, 500:575]
    away_team = score_box[40:165, 750:850]

    return away_score, away_team, home_score, home_team


if __name__ == "__main__":
    first_period_temp = cv2.imread("templates/first-period-temp.jeg", 0)
    first_period_temp = cv2.Canny(first_period_temp, 50, 200)
    first_intermission_temp = cv2.imread("templates/first-intermission-temp.jpg", 0)
    first_intermission_temp = cv2.Canny(first_intermission_temp, 50, 200)
    second_period_temp = cv2.imread("templates/second-period-temp.jpg", 0)
    second_period_temp = cv2.Canny(second_period_temp, 50, 200)
    second_intermission_temp = cv2.imread("templates/second-intermission-temp.jpg", 0)
    second_intermission_temp = cv2.Canny(second_intermission_temp, 50, 200)
    third_period_temp = cv2.imread("templates/third-period-template.jpg", 0)
    third_period_temp = cv2.Canny(third_period_temp, 50, 200)
    third_intermission_temp = cv2.imread("templates/third-intermission-template.jpg", 0)
    third_intermission_temp = cv2.Canny(third_intermission_temp, 50, 200)
    score_box_temp = cv2.imread("templates/score-box-template.jpg", 0)
    score_box_temp = cv2.Canny(score_box_temp, 50, 200)

    templates = [
        first_period_temp,
        first_intermission_temp,
        second_period_temp,
        second_intermission_temp,
        third_period_temp,
        third_intermission_temp
    ]

    image = cv2.imread("Example Photos/first-intermission-replay-1.jpeg", 0)
    print(templates)

    # camera = picamera.PiCamera()
    # camera.shutter_speed = 10000
    # camera.brightness = 50
    # camera.exposure_mode = "off"
    # camera.drc_strength = 'high'

    game_complete = False
    while game_complete is not True:
        result = read_pause_menu(image, score_box_temp, templates, 0.5)
        if result == 0:
            print("False")
        elif result == 1:
            game_complete == True
    away_score, away_team, home_score, home_team = crop_image(image)
    stats = []
    for item in [home_team, away_team]:
        stat = read_image(item, 'name')
        stats.append(stat)

    for item in [home_score, away_score]:
        stat = read_image(item, 'score')

    stats.append(stat)
