import io
import numpy as np
import picamera
import picamera.array
import cv2
import pytesseract
import time


def read_pause_menu(image):
    imgray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    canny = cv2.Canny(imgray, 50, 200)
    score_res = cv2.matchTemplate(canny, score_box_temp, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(score_res)
    print('Score box max val', max_val)
    if max_val > 0.5:
        print("Score box found")
        templates = [
            first_period_temp,
            first_intermission_temp,
            second_period_temp,
            second_intermission_temp,
            third_period_temp,
            third_intermission_temp
        ]
        matches = []
        for temp in templates:
            match = cv2.matchTemplate(canny, temp, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
            print('Template max val:', max_val)
            matches.append(max_val)
        for mat in matches:
            if mat > .5:
                return 0
        return 1


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
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (4, 4))
    dilated = cv2.dilate(thresh, kernel, iterations=5)
    img, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    area_list = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        area_list.append(area)
    area_list_sort = sorted(area_list)
    x, y, w, h = cv2.boundingRect(contours[-1])
    roi_clean = thresh[y:y + h, x:x + w]

    if type.lower() == 'name':
        cv2.imshow('image', roi_clean)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        text = pytesseract.image_to_string(roi_clean,
                                           config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 7 -oem 2 no_dict")
    elif type.lower() == 'score':
        cv2.imshow('image', roi_clean)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        text = pytesseract.image_to_string(roi_clean, config="-c tessedit_char_whitelist=1234567890 -psm 6")
    return (text)


if __name__ == "__main__":
    first_period_temp = cv2.imread("templates/first-period-template.jpeg", 0)
    first_period_temp = cv2.Canny(first_period_temp, 50, 200)
    first_intermission_temp = cv2.imread("templates/first-intermission-template.jpeg", 0)
    first_intermission_temp = cv2.Canny(first_intermission_temp, 50, 200)
    second_period_temp = cv2.imread("templates/second-period-template.jpeg", 0)
    second_period_temp = cv2.Canny(second_period_temp, 50, 200)
    second_intermission_temp = cv2.imread("templates/second-intermission-template.jpeg", 0)
    second_intermission_temp = cv2.Canny(second_intermission_temp, 50, 200)
    third_period_temp = cv2.imread("templates/third-period-template.jpeg", 0)
    third_period_temp = cv2.Canny(third_period_temp, 50, 200)
    third_intermission_temp = cv2.imread("templates/third-intermission-template.jpeg", 0)
    third_intermission_temp = cv2.Canny(third_intermission_temp, 50, 200)
    score_box_temp = cv2.imread("templates/score-box-template.jpeg", 0)
    score_box_temp = cv2.Canny(score_box_temp, 50, 200)

    camera = picamera.PiCamera()
    camera.shutter_speed = 10000
    camera.brightness = 50
    camera.exposure_mode = "off"
    camera.drc_strength = 'high'

    game_complete = False
    while game_complete is not True:
        rawCapture = picamera.array.PiRGBArray(camera)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        time.sleep(.5)
        result = read_pause_menu(image)
        if result == 1:
            game_complete = True
        print(game_complete)
        rawCapture.truncate(0)
    print("image found!")
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

    stats = []
    for item in [home_team, away_team]:
        stat = read_image(item, 'name')
        stats.append(stat)

    for item in [home_score, away_score]:
        stat = read_image(item, 'score')
        stats.append(stat)
    print(stats)
