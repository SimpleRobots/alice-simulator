import cv2
import numpy as np


def rect(x0, y0, w, h):
    return [((x0, y0), (x0, y0 + h)),
            ((x0, y0 + h), (x0 + w, y0 + h)),
            ((x0 + w, y0 + h), (x0 + w, y0)),
            ((x0 + w, y0), (x0, y0))
            ]


def _calc_bbox(lines):
    min_p_x = lines[0][0][0]
    min_p_y = lines[0][0][1]
    max_p_x = lines[0][0][0]
    max_p_y = lines[0][0][1]

    for i in range(len(lines)):
        for j in range(2):
            min_p_x = min(min_p_x, lines[i][j][0])
            min_p_y = min(min_p_y, lines[i][j][1])
            max_p_x = max(max_p_x, lines[i][j][0])
            max_p_y = max(max_p_y, lines[i][j][1])

    return (min_p_x, min_p_y), (max_p_x, max_p_y)


def render(lines):
    bbox = _calc_bbox(lines)

    scale = 100.0  # pixels per meter
    color = (0, 0, 0)
    width = 2

    w = int((bbox[1][0]) * scale)
    h = int((bbox[1][1]) * scale)
    img = np.zeros((h, w, 3), np.uint8)
    img[:, :, :] = 255

    for line in lines:
        x1, y1 = line[0]
        x2, y2 = line[1]
        start = (int(x1 * scale), int(h - y1 * scale))
        end = (int(x2 * scale), int(h - y2 * scale))
        cv2.line(img, start, end, color, width)

    return img


def display(img):
    cv2.imshow("debug", img)
    cv2.waitKey(0)
