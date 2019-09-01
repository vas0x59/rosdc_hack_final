import cv2


def draw_boxes(img, boxes, ids, confs, CLASSES, COLORS=None):
    for i in range(len(boxes)):
        # extract the bounding box coordinates
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])
        # x /= 0.35
        # y /= 0.35
        # w /= 0.35
        # h /= 0.35
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)
        color = (0, 255, 150)
        if COLORS is not None:
            color = [int(c) for c in COLORS[ids[i]]]

        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        text = "{}: {:.4f}".format(CLASSES[ids[i]], confs[i])
        cv2.putText(img, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 2)
    return img
