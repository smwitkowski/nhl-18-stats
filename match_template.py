import cv2


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


def match_templates(image, score_template, pause_templates, threshold, gray_image):
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
