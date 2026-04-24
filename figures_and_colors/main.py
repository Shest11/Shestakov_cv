import cv2

image = cv2.imread("balls_and_rects.png")

img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
hue_img = img_hsv[:, :, 0]

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

rect_dict = {}
circ_dict = {}

for coord in contours:
    x, y, w, h = cv2.boundingRect(coord)
    y_center = h // 2 + y
    x_center = w // 2 + x
    hue = hue_img[y_center, x_center]
    if len(coord) > 4:
        if hue not in circ_dict:
            circ_dict[hue] = 0
        circ_dict[hue] += 1
    else:
        if hue not in rect_dict:
            rect_dict[hue] = 0
        rect_dict[hue] += 1

print(f"Кол-во фигур: {len(contours)}")

cnt = 1
print("Прямоугольников: ")
for key in sorted(rect_dict):
    print(f"{cnt} оттенок: {rect_dict[key]} шт")
    cnt += 1

cnt = 1
print("Кружков: ")
for key in sorted(circ_dict):
    print(f"{cnt} оттенок: {circ_dict[key]} шт")
    cnt += 1