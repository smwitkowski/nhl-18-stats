import cv2


def find_template(image, templates):
    matches = []
    for temp in templates:
        match = cv2.matchTemplate(image, temp, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
        matches.append(max_val)
    return max(matches)


def read_pause_menu(image, score_template, pause_templates, threshold, gray_image):
    # The threshold is a percent, and needs to be between 0 and 1.
    # If it's not, return an error message to the user
    if threshold > 1:
        return "Please provide a number between 0 and 1 for the threshold."

    # If the user speified that the image is not already gray, convert it to grey
    if not gray_image:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert the score 
    canny = cv2.Canny(image, 50, 200)
    score_val = find_template(canny, score_template)
    if score_val > threshold:
        pause_val = find_template(canny, pause_templates)
        if pause_val < threshold:
            return 1


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
