import cv2
import pytesseract


def find_template(image, templates):
    # Create an empty list
    # This list will be populated with the max value from each template
    matches = []

    # Loop through the templates provided
    # Note: It's OK if only one template is provided
    for temp in templates:
        # Match the template to the image the user provided
        match = cv2.matchTemplate(image, temp, cv2.TM_CCOEFF_NORMED)

        # Extract values using minMacLoc on the match created above
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)

        # Append the max value to the matches list created outside the loop
        matches.append(max_val)

    # Return the largest value in the matches list
    return max(matches)


def read_pause_menu(image, score_template, pause_templates, threshold, gray_image):
    # The threshold is a percent, and needs to be between 0 and 1.
    # If it's not, return an error message to the user
    if threshold > 1:
        return "Please provide a number between 0 and 1 for the threshold."

    # If the user specified that the image is not already gray, convert it to grey
    if not gray_image:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert the image to a canny outline
    canny = cv2.Canny(image, 50, 200)

    # find_template returns the highest value matching the templates provided.
    # In this case, only the score template is provided.
    # This returns the max_val for the match to the score box template.
    score_val = find_template(canny, score_template)

    # Continue if score_val is greater than the threshold set by the user
    if score_val > threshold:

        # Loop through all the pause templates (defined by the user) and match the templates to the image
        # Return the highest matching value of all the templates
        pause_val = find_template(canny, pause_templates)

        # If the value is below the threshold, then the template is not present.
        # If this is true for all the templates, then we know the game has ended and is not just paused.
        if pause_val < threshold:
            return 1
    else:
        return 0

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
    area_list_sort = sorted(area_list)
    x, y, w, h = cv2.boundingRect(area_list_sort[-1])
    return x, y, w, h


def read_team_and_score(image, gray_image):
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


def read_image(image, type):
    # Apply adaptive thresholding to the image
    # The image 'lighting; will rarely change.
    # TODO change the adaptiveThreshold to threshold
    thresh = cv2.adaptiveThreshold(image,
                                   255,
                                   cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV,
                                   31,
                                   21)

    # If the image type is the team name, then continue
    if type.lower() == "name":
        #
        image_iso = read_name(thresh)
        text = pytesseract.image_to_string(image_iso,
                                           config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 7 -oem 2 no_dict")
        return text
    elif type.lower() == 'score':
        text = pytesseract.image_to_string(image_iso, config="-c tessedit_char_whitelist=1234567890 -psm 6")
        return text
    else:
        return "Please define the type of picture. It's either a 'name' or 'score'."



