import cv2
import pytesseract


def find_largest_area(contours):
    # Create an empty list that will be populated later
    area_list = []

    # Loop through the contours given by the user
    for cnt in contours:
        # Find the area based on the values provided by boundingRect
        # Append to the list created above
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        area_list.append(area)

    # Sort the list and return the x, y, w, and h values for the contour with the largest area
    x, y, w, h = cv2.boundingRect(contours[area_list.index(max(area_list, default=0))])
    return x, y, w, h


def crop_team_and_score(image, gray_image):
    # If the user specified that the image is not already gray, convert it to gray
    if not gray_image:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert the image to black and white using a threshold
    _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)

    # Find all the contours of the newly threshed image
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour of the contours provided.
    # This is used to identify the score box
    # TODO Use template matching to identify the scorebox, instead of size of contours
    x, y, w, h = find_largest_area(contours)

    # Crop the image to the area defined in the function above and resize
    score_box = image[y:y + h, x:x + w]
    score_box = cv2.resize(score_box, (1000, 1000))

    # Crop the image for each item of interest
    # I tested the X and Y coordinates to find the correct location, but it could be done in a different way.
    home_score = score_box[40:220, 400:475]
    home_team = score_box[40:165, 150:250]
    away_score = score_box[40:220, 500:575]
    away_team = score_box[40:165, 750:850]

    return away_score, away_team, home_score, home_team


def read_name(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (4, 4))
    dilated = cv2.dilate(image, kernel, iterations=5)
    img, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = find_largest_area(contours)
    cropped = image[y:y + h, x:x + w]
    return cropped


def read_stats(image, type):
    # Apply adaptive thresholding to the image
    # The image 'lighting; will rarely change.
    # TODO change the adaptiveThreshold to threshold
    thresh = cv2.adaptiveThreshold(image,
                                   255,
                                   cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV,
                                   31,
                                   21)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    eroded = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    # If the image type is the team name, then continue
    if type.lower() == "name":
        # read_name returns a cropped image of the file
        # TODO Make the cropped images more accurate so cropping is unneccesary
        image_iso = read_name(eroded)

        # Use tesseract to read the cropped image.
        # The configuration only allows letters to be returned.
        # In addition, no_dict removes the dictionary requirement so team abbreviations can be read
        text = pytesseract.image_to_string(image_iso,
                                           config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 7 -oem 2 no_dict")
        return text

    # If the image type is the team score, then continue
    elif type.lower() == 'score':
        # Use tesseract to read the cropped image.
        # The configuration only allows numbers to be returned.
        text = pytesseract.image_to_string(eroded, config="-c tessedit_char_whitelist=1234567890 -psm 6")
        return text
    else:
        return "Please define the type of picture. It's either a 'name' or 'score'."
