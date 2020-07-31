import cv2 as cv

def draw_points(data, frame):
    lines = data["lines"]
    points = data["points"]

    for pair in points:
        # draw an 'x' for the keypoint pair
        x, y = pair[0], pair[1]
        cv.line(frame, (x, y), (x + 10, y + 10), (0, 0, 255), 8)
        cv.line(frame, (x, y + 10), (x + 10, y), (0, 0, 255), 8)

    for line in lines:
        # draw two lines showing the connection between points
        x1, y1, x2, y2 = line[0], line[1], line[2], line[3]
        cv.line(frame, (x1, y1), (x1, y2), (0, 0, 255), 6)
        cv.line(frame, (x1, y2), (x2, y2), (0, 0, 255), 6)
