import cv2


def read_template_files():
    first_period_temp = cv2.imread("templates/first-period-temp.jpg", 0)
    first_period_temp = cv2.Canny(first_period_temp, 50, 200)
    first_intermission_temp = cv2.imread("templates/first-intermission-temp.jpg", 0)
    first_intermission_temp = cv2.Canny(first_intermission_temp, 50, 200)
    second_period_temp = cv2.imread("templates/second-period-temp.jpg", 0)
    second_period_temp = cv2.Canny(second_period_temp, 50, 200)
    second_intermission_temp = cv2.imread("templates/second-intermission-temp.jpg", 0)
    second_intermission_temp = cv2.Canny(second_intermission_temp, 50, 200)
    third_period_temp = cv2.imread("templates/third-period-temp.jpg", 0)
    third_period_temp = cv2.Canny(third_period_temp, 50, 200)
    # third_intermission_temp = cv2.imread("templates/third-intermission-template.jpg", 0)
    # third_intermission_temp = cv2.Canny(third_intermission_temp, 50, 200)
    score_box_temp = cv2.imread("templates/score-box-temp.jpeg", 0)
    score_box_temp = cv2.Canny(score_box_temp, 50, 200)

    templates = [
        first_period_temp,
        first_intermission_temp,
        second_period_temp,
        second_intermission_temp,
        third_period_temp
    ]

    return templates, score_box_temp


def find_template(image, temp):
    # Create an empty list
    # This list will be populated with the max value from each template
    matches = []
    # locs = []

    # Loop through the templates provided
    # Note: It's OK if only one template is provided
    match = cv2.matchTemplate(image, temp, cv2.TM_CCOEFF_NORMED)
    # Extract values using minMacLoc on the match created above

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
    # Append the max value to the matches list created outside the loop

    matches.append(max_val)
    print(max_val)

    # Return the largest value in the matches list
    return max(matches)


def find_templates(image, temps):
    # Create an empty list
    # This list will be populated with the max value from each template
    matches = []
    # locs = []

    # Loop through the templates provided
    # Note: It's OK if only one template is provided
    for temp in temps:
        # Match the template to the image the user provided
        match = cv2.matchTemplate(image, temp, cv2.TM_CCOEFF_NORMED)

        # Extract values using minMacLoc on the match created above
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)

        # Append the max value to the matches list created outside the loop
        matches.append(max_val)
        print(max_val)
        #locs.append(max_loc)

    # Return the largest value in the matches list
    return max(matches)


def match_templates(image, score_template, pause_templates, gray_image):

    # If the user specified that the image is not already gray, convert it to grey
    if not gray_image:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert the image to a canny outlin
    canny = cv2.Canny(image, 50, 200)

    # find_template returns the highest value matching the templates provided.
    # In this case, only the score template is provided.
    # This returns the max_val for the match to the score box template.
    score_val = find_template(canny, score_template)

    # Continue if score_val is greater than the threshold set by the user
    if score_val > .35:
        # top_left = score_loc
        # x, y, w, h = score_template.shape()
        # bottom_right = (top_left[0] + w, top_left[1] + h)
        #cv2.rectangle(canny, top_left, bottom_right, 255, 2)
        # Loop through all the pause templates (defined by the user) and match the templates to the image
        # Return the highest matching value of all the templates
        pause_val = find_templates(canny, pause_templates)

        # If the value is below the threshold, then the template is not present.
        # If this is true for all the templates, then we know the game has ended and is not just paused.
        if pause_val < .5:
            return 1
        else:
            # top_left = pause_loc
            # x, y, w, h = pause_templates[pause_templates.index(pause_val)].shape()
            # bottom_right = (top_left[0] + w, top_left[1] + h)
            # cv2.rectangle(canny, top_left, bottom_right, 255, 2)
            #cv2.imshow("Canny Matches", canny)
            return 0
    else:
        return 0
