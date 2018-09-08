import cv2


def read_templat_files():
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
    print(max(matches))
    return max(matches)


def match_templates(image, score_template, pause_templates, gray_image):

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
    if score_val > .35:

        # Loop through all the pause templates (defined by the user) and match the templates to the image
        # Return the highest matching value of all the templates
        pause_val = find_template(canny, pause_templates)

        # If the value is below the threshold, then the template is not present.
        # If this is true for all the templates, then we know the game has ended and is not just paused.
        if pause_val < .5:
            return 1
        else:
            return 0
    else:
        return 0
